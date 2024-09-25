from supabase import create_client, Client

url: str = "https://jhtxzmjribqxtapgvulw.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpodHh6bWpyaWJxeHRhcGd2dWx3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzNjU3MjgsImV4cCI6MjA0MDk0MTcyOH0.dYB3t2ZLtblz7aTpV9tmmtD1rAzqcYFFcIcL64qyR3Q"

supabase: Client = create_client(url, key)