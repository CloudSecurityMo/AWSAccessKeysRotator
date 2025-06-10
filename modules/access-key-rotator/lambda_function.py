
import boto3
import json
import logging
from datetime import datetime, timezone, timedelta
import os

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to disable AWS access keys older than specified days
    """
    
    # Get configuration from environment variables
    max_key_age_days = int(os.environ.get('MAX_KEY_AGE_DAYS', 90))
    
    # Initialize IAM client
    iam_client = boto3.client('iam')
    
    try:
        # Get all IAM users
        paginator = iam_client.get_paginator('list_users')
        
        disabled_keys = []
        total_keys_checked = 0
        
        for page in paginator.paginate():
            for user in page['Users']:
                username = user['UserName']
                logger.info(f"Checking access keys for user: {username}")
                
                # Get access keys for the user
                try:
                    access_keys_response = iam_client.list_access_keys(UserName=username)
                    
                    for key_metadata in access_keys_response['AccessKeyMetadata']:
                        access_key_id = key_metadata['AccessKeyId']
                        key_status = key_metadata['Status']
                        key_create_date = key_metadata['CreateDate']
                        
                        total_keys_checked += 1
                        
                        # Skip if key is already inactive
                        if key_status == 'Inactive':
                            logger.info(f"Access key {access_key_id} for user {username} is already inactive")
                            continue
                        
                        # Calculate key age
                        key_age = datetime.now(timezone.utc) - key_create_date
                        key_age_days = key_age.days
                        
                        logger.info(f"Access key {access_key_id} for user {username} is {key_age_days} days old")
                        
                        # Disable key if it's older than max_key_age_days
                        if key_age_days >= max_key_age_days:
                            try:
                                # Get last used information for logging
                                try:
                                    last_used_response = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
                                    last_used = last_used_response.get('AccessKeyLastUsed', {}).get('LastUsedDate', 'Never')
                                except Exception as e:
                                    last_used = 'Unknown'
                                    logger.warning(f"Could not get last used date for key {access_key_id}: {str(e)}")
                                
                                # Disable the access key
                                iam_client.update_access_key(
                                    UserName=username,
                                    AccessKeyId=access_key_id,
                                    Status='Inactive'
                                )
                                
                                disabled_key_info = {
                                    'username': username,
                                    'access_key_id': access_key_id,
                                    'age_days': key_age_days,
                                    'last_used': str(last_used),
                                    'created_date': str(key_create_date)
                                }
                                disabled_keys.append(disabled_key_info)
                                
                                logger.info(f"Disabled access key {access_key_id} for user {username} (age: {key_age_days} days)")
                                
                            except Exception as e:
                                logger.error(f"Failed to disable access key {access_key_id} for user {username}: {str(e)}")
                        
                except Exception as e:
                    logger.error(f"Failed to list access keys for user {username}: {str(e)}")
        
        # Prepare response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Access key rotation completed successfully',
                'total_keys_checked': total_keys_checked,
                'keys_disabled': len(disabled_keys),
                'disabled_keys': disabled_keys,
                'max_key_age_days': max_key_age_days
            }, default=str)
        }
        
        logger.info(f"Rotation completed. Checked {total_keys_checked} keys, disabled {len(disabled_keys)} keys")
        
        return response
        
    except Exception as e:
        logger.error(f"Error during access key rotation: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Access key rotation failed: {str(e)}'
            })
        }
