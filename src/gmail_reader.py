"""
Gmail Reader Module - Core functionality for reading and processing Gmail messages.

This module provides methods to authenticate with Gmail API, fetch emails,
and extract relevant information for voice processing.
"""

import os
import pickle
import logging
from typing import List, Dict, Optional
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailReader:
    """
    A class to handle Gmail API interactions and email retrieval.
    
    Attributes:
        service: Google API service object
        user_id: Gmail user ID (typically 'me')
    """
    
    def __init__(self):
        """Initialize GmailReader with API configuration."""
        self.service = None
        self.user_id = 'me'
        self.credentials_path = 'credentials.json'
        self.token_path = 'token.pickle'
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth 2.0.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            creds = None
            
            # Load existing token if available
            if os.path.exists(self.token_path):
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for future use
                with open(self.token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = discovery.build('gmail', 'v1', credentials=creds)
            logger.info("Gmail authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def get_latest_emails(self, count: int = 5, query: str = '') -> List[Dict]:
        """
        Fetch latest emails from Gmail inbox.
        
        Args:
            count: Number of emails to fetch
            query: Gmail search query (e.g., 'from:sender@email.com')
        
        Returns:
            List of email dictionaries with sender, subject, and body
        """
        try:
            # Build query
            query_str = query or 'is:unread'
            
            # Get message IDs
            results = self.service.users().messages().list(
                userId=self.user_id,
                q=query_str,
                maxResults=count
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self._get_message_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except Exception as e:
            logger.error(f"Failed to fetch emails: {str(e)}")
            return []
    
    def _get_message_details(self, message_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific message.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Dictionary with message details or None if failed
        """
        try:
            message = self.service.users().messages().get(
                userId=self.user_id,
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            body = self._get_message_body(message['payload'])
            
            return {
                'id': message_id,
                'sender': sender,
                'subject': subject,
                'body': body,
                'date': date,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get message details: {str(e)}")
            return None
    
    @staticmethod
    def _get_message_body(payload: Dict) -> str:
        """
        Extract message body from payload.
        
        Args:
            payload: Message payload dictionary
        
        Returns:
            Decoded message body text
        """
        try:
            if 'parts' in payload:
                # Message has multiple parts
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        return base64.urlsafe_b64decode(data).decode('utf-8')
            else:
                # Simple message
                data = payload['body'].get('data', '')
                return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to decode message body: {str(e)}")
            return ""
    
    def search_emails(self, query: str) -> List[Dict]:
        """
        Search for emails using Gmail search syntax.
        
        Args:
            query: Gmail search query
        
        Returns:
            List of matching emails
        """
        return self.get_latest_emails(count=10, query=query)
    
    def get_email_by_id(self, message_id: str) -> Optional[Dict]:
        """
        Get a specific email by ID.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Email dictionary or None
        """
        return self._get_message_details(message_id)


if __name__ == '__main__':
    # Example usage
    reader = GmailReader()
    
    if reader.authenticate():
        emails = reader.get_latest_emails(count=3)
        
        for email in emails:
            print(f"From: {email['sender']}")
            print(f"Subject: {email['subject']}")
            print(f"Body: {email['body'][:100]}...")
            print("-" * 50)