from supabase import create_client, Client

url: str = "https://clvvpgmntfgznsahgrar.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsdnZwZ21udGZnem5zYWhncmFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzNzgzNzcsImV4cCI6MjA0MDk1NDM3N30.mLbfZ0gWMQaQEsswfHkgJ17p7fnYhk0mWYsDJkuf5Qs"
supabase: Client = create_client(url, key)