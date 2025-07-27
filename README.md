# Concordia IEEE Notion Supabase API

A unified FastAPI server that provides access to both Supabase database and Notion workspace data through a single API interface. Built for the IEEE Concordia student branch to streamline data access across multiple platforms.

## Features

- 🚀 **FastAPI** - Modern, fast web framework with automatic API documentation
- 🗄️ **Supabase Integration** - Full access to your Supabase database tables
- 📝 **Notion Integration** - Query Notion databases and pages
- 🔍 **Automatic API Docs** - Interactive Swagger UI at `/docs`
- 🔐 **Environment-based Configuration** - Secure credential management
- 🛠️ **Debug Endpoints** - Built-in debugging tools for troubleshooting connections

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Supabase project with API credentials
- Notion integration token and database access

### Installation

1. **Clone and create virtual environment**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   python3 -m venv ieee
   source ieee/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
   
   # Notion Configuration
   NOTION_TOKEN=your-notion-integration-token
   NOTION_DATABASE_ID=your-database-id-with-dashes
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the API**
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/

## Configuration Guide

### Supabase Setup

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Navigate to **Settings** → **API**
3. Copy your **URL** and **anon key**
4. For admin access, also copy the **service_role key**

### Notion Setup

1. Create a Notion integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Copy the **Internal Integration Token**
3. Share your database with the integration:
   - Go to your Notion database
   - Click **"..."** → **"Add connections"**
   - Select your integration
4. Get the database ID from your database URL:
   ```
   https://notion.so/workspace/DATABASE_ID?v=VIEW_ID
   ```
   Format it with dashes: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## API Endpoints

### Health & Debug

- `GET /` - Health check
- `GET /debug/connection` - Test Supabase connection
- `GET /debug/notion` - Test Notion connection

### Supabase Data

- `GET /users` - Get all users
- `GET /users/{user_id}` - Get specific user by ID
- `GET /users/search?email={email}&first_name={name}` - Search users
- `GET /tables/{table_name}` - Get data from any table
- `GET /tables/{table_name}/count` - Get row count for a table
- `GET /inventory/tables` - List all available tables

### Notion Data

- `GET /notion/database` - Query Notion database
- `GET /notion/pages` - Get all pages from database

## Available Tables

Your Supabase database includes:
- `User` - User accounts and profiles
- `InventoryItem` - Equipment and inventory tracking
- `Organization` - IEEE branch organizations
- `Location` - Physical locations
- `Team Member` - Team assignments
- And many more...

## Example Usage

### Get All Users
```bash
curl "http://localhost:8000/users?limit=50"
```

### Search Users by Email
```bash
curl "http://localhost:8000/users/search?email=gmail.com"
```

### Get Inventory Items
```bash
curl "http://localhost:8000/tables/InventoryItem"
```

### Query Notion Database
```bash
curl "http://localhost:8000/notion/database"
```

## Development

### Project Structure
```
.
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment file
└── README.md           # This file
```

### Adding New Endpoints

The application is designed to be easily extensible. To add new endpoints:

1. Follow the existing pattern in `main.py`
2. Use the existing Supabase or Notion clients
3. Add proper error handling and response formatting

### Debugging

Use the built-in debug endpoints to troubleshoot:

- `/debug/connection` - Verify Supabase connection and RLS policies
- `/debug/notion` - Test Notion API access and permissions

## Common Issues

### Empty Supabase Results
- **Cause**: Row Level Security (RLS) policies blocking access
- **Solution**: Use service_role key or configure RLS policies

### Notion Connection Errors
- **Cause**: Integration not shared with database
- **Solution**: Add your integration to the database connections

### Port Already in Use
```bash
# Kill process on port 8000
kill $(lsof -ti :8000)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For questions or issues:
- Create an issue in this repository
- Contact the IEEE Concordia tech team
- Check the FastAPI docs at `/docs` for API usage

---

Built with ❤️ for IEEE Concordia University
