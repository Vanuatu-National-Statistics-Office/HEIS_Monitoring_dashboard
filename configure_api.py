"""
Survey Solutions API Configuration Helper
==========================================
This script helps you configure the dashboard to automatically 
extract data from the Survey Solutions server.
"""

import os
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("🌐 Survey Solutions API Configuration")
    print("="*60)
    print("\nThis will configure automatic data extraction from:")
    print("📡 Server: https://vnsocapi.gov.vu/")
    print("\n" + "="*60 + "\n")
    
    # Get current .env path
    env_path = Path(__file__).parent / '.env'
    
    # Check if .env exists
    if not env_path.exists():
        print("⚠️  .env file not found. Creating from template...\n")
        env_example = Path(__file__).parent / '.env.example'
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_path)
            print("✅ Created .env file\n")
        else:
            print("❌ Error: .env.example not found")
            return
    
    # Get credentials
    print("📝 Enter your Survey Solutions API credentials:")
    print("   (Contact your administrator if you don't have these)\n")
    
    username = input("API Username: ").strip()
    if not username:
        print("❌ Username is required. Exiting.")
        return
    
    password = input("API Password: ").strip()
    if not password:
        print("❌ Password is required. Exiting.")
        return
    
    # Read current .env content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update the relevant lines
    new_lines = []
    updated_source = False
    updated_user = False
    updated_pass = False
    
    for line in lines:
        if line.startswith('DATA_SOURCE='):
            new_lines.append('DATA_SOURCE=api\n')
            updated_source = True
        elif line.startswith('SS_API_USER='):
            new_lines.append(f'SS_API_USER={username}\n')
            updated_user = True
        elif line.startswith('SS_API_PASSWORD='):
            new_lines.append(f'SS_API_PASSWORD={password}\n')
            updated_pass = True
        else:
            new_lines.append(line)
    
    # Add missing lines if they weren't in the file
    if not updated_source:
        new_lines.append('\nDATA_SOURCE=api\n')
    if not updated_user:
        new_lines.append(f'SS_API_USER={username}\n')
    if not updated_pass:
        new_lines.append(f'SS_API_PASSWORD={password}\n')
    
    # Write updated .env
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print("\n" + "="*60)
    print("✅ Configuration saved successfully!")
    print("="*60)
    print("\n📋 Configuration Summary:")
    print(f"   Data Source: API (automatic extraction)")
    print(f"   Server: https://vnsocapi.gov.vu/")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password)}")
    
    print("\n" + "="*60)
    print("🚀 Next Steps:")
    print("="*60)
    print("1. Start the Flask server:")
    print("   python app.py")
    print("\n2. Check the console output for:")
    print("   ✅ Successfully loaded X records from API")
    print("\n3. Open your browser:")
    print("   http://127.0.0.1:5000")
    print("\n4. If connection fails:")
    print("   - Check your credentials")
    print("   - Verify network connection")
    print("   - Contact your Survey Solutions administrator")
    print("\n" + "="*60)
    print("📚 For more help, see: OPTION_B_API_SETUP.md")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please check the error and try again.")
