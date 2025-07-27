import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client
from notion_client import Client as NotionClient

# Load environment variables
print("Loading environment variables...")
load_dotenv()


# Initialize FastAPI
print("Starting Supabase Data API...")
app = FastAPI(
    title="Supabase Data API",
    description="Mini API server for Supabase data",
    version="1.0.0"
)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

notion_token = os.getenv("NOTION_TOKEN")
notion_database_id = os.getenv("NOTION_DATABASE_ID")

print("Creating Supabase client...")
if not supabase_url or not supabase_key:
    print("Environment variables SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set.")
    exit(1)
else:
    supabase: Client = create_client(supabase_url, supabase_key)
    print("Supabase client created successfully.")

print("Creating Notion client...")
if notion_token:
    notion = NotionClient(auth=notion_token)
    print("Notion client created successfully.")
else:
    print("NOTION_TOKEN not found - Notion endpoints will be disabled")
    notion = None



@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Supabase Data API is running", "status": "healthy"}

@app.get("/tables/{table_name}")
async def get_table_data(table_name: str, limit: int = 100):
    """Get data from any table with optional limit"""
    try:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        return {
            "table": table_name,
            "count": len(response.data),
            "data": response.data
        }
    except Exception as e:
        return {"error": str(e), "table": table_name}

@app.get("/tables")
async def get_all_tables():
    """Get list of all tables in the database"""
    try:
        response = supabase.rpc('get_tables_info').execute()
        
        if not response.data:
            query = """
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
            response = supabase.rpc('sql_query', {'query': query}).execute()
        
        return {
            "tables": response.data,
            "count": len(response.data) if response.data else 0
        }
    except Exception as e:
        return {
            "error": "Could not fetch table list",
            "message": str(e),
            "suggestion": "Use /tables/{table_name} if you know your table names"
        }

@app.get("/users")
async def get_all_users(limit: int = 100):
    """Get all users with optional limit"""
    try:
        response = supabase.table("User").select("*").limit(limit).execute()
        return {
            "users": response.data,
            "count": len(response.data)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    """Get specific user by ID"""
    try:
        response = supabase.table("User").select("*").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/users/search")
async def search_users(email: str = "", first_name: str = ""):
    """Search users by email or first name"""
    try:
        query = supabase.table("User").select("*")
        
        if email:
            query = query.ilike("email", f"%{email}%")
        if first_name:
            query = query.ilike("firstName", f"%{first_name}%")
            
        response = query.execute()
        return {
            "users": response.data,
            "count": len(response.data)
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/debug/connection")
async def debug_connection():
    """Debug Supabase connection and permissions"""
    results = {}
    
    # Test basic connection
    try:
        response = supabase.table("User").select("count", count="exact").execute()
        results["connection"] = "✅ Connected"
        results["total_count"] = response.count
    except Exception as e:
        results["connection"] = f"❌ Error: {str(e)}"
    
    # Test with different table names
    for table_name in ["User", "user", "users"]:
        try:
            response = supabase.table(table_name).select("*").limit(1).execute()
            results[f"table_{table_name}"] = f"✅ Found {len(response.data)} rows"
        except Exception as e:
            results[f"table_{table_name}"] = f"❌ {str(e)}"
    
    return results



@app.get("/debug/notion")
async def debug_notion():
    """Test Notion connection and database access"""
    if not notion:
        return {"error": "Notion client not initialized"}
    
    try:
        # Test database access
        response = notion.databases.query(database_id=notion_database_id)
        return {
            "status": "✅ Connected to Notion",
            "database_id": notion_database_id,
            "results_count": len(response.get("results", [])),
            "sample_page": response.get("results", [{}])[0].get("properties", {}) if response.get("results") else "No pages found"
        }
    except Exception as e:
        return {"error": f"❌ {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
