#!/usr/bin/env python3
"""
CSV Processor Deployment Helper
This script helps you deploy to various free platforms.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print deployment banner"""
    print("🚀 CSV Processor - Free Deployment Helper")
    print("=" * 50)

def check_git_repo():
    """Check if this is a git repository"""
    if not os.path.exists('.git'):
        print("⚠️  This is not a git repository.")
        print("   Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository found")

def check_requirements():
    """Check if requirements.txt exists"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    print("✅ requirements.txt found")
    return True

def show_deployment_options():
    """Show deployment options"""
    print("\n🌐 Choose your deployment platform:")
    print("1. Railway (Recommended) - Easiest")
    print("2. Render - Great for beginners")
    print("3. Heroku - Classic choice")
    print("4. Fly.io - Developer-friendly")
    print("5. Vercel - Frontend-focused")
    print("6. Show all options")

def deploy_railway():
    """Deploy to Railway"""
    print("\n🚂 Deploying to Railway...")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose this repository")
    print("6. Railway will auto-detect Python and deploy!")
    
    choice = input("\nOpen Railway in browser? (y/n): ")
    if choice.lower() == 'y':
        webbrowser.open('https://railway.app')

def deploy_render():
    """Deploy to Render"""
    print("\n🎨 Deploying to Render...")
    print("1. Go to https://render.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your GitHub repo")
    print("5. Configure:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT")
    print("6. Click 'Deploy'")
    
    choice = input("\nOpen Render in browser? (y/n): ")
    if choice.lower() == 'y':
        webbrowser.open('https://render.com')

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n🟣 Deploying to Heroku...")
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        print("✅ Heroku CLI found")
        
        # Create Heroku app
        app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
        if not app_name:
            app_name = "csv-processor-" + str(hash(os.getcwd()))[-6:]
        
        print(f"Creating Heroku app: {app_name}")
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        print("Deploying to Heroku...")
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy CSV Processor'], check=True)
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        print(f"✅ Deployed! Your app is at: https://{app_name}.herokuapp.com")
        
    except subprocess.CalledProcessError:
        print("❌ Heroku CLI not found. Please install it first:")
        print("   https://devcenter.heroku.com/articles/heroku-cli")
    except FileNotFoundError:
        print("❌ Heroku CLI not found. Please install it first:")
        print("   https://devcenter.heroku.com/articles/heroku-cli")

def deploy_fly():
    """Deploy to Fly.io"""
    print("\n🪰 Deploying to Fly.io...")
    
    try:
        subprocess.run(['fly', '--version'], check=True, capture_output=True)
        print("✅ Fly CLI found")
        
        print("Launching on Fly.io...")
        subprocess.run(['fly', 'launch'], check=True)
        print("✅ Deployed to Fly.io!")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Fly CLI not found. Please install it first:")
        print("   https://fly.io/docs/hands-on/install-flyctl/")

def deploy_vercel():
    """Deploy to Vercel"""
    print("\n▲ Deploying to Vercel...")
    print("1. Go to https://vercel.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Import your GitHub repository")
    print("5. Vercel will auto-detect and deploy!")
    
    choice = input("\nOpen Vercel in browser? (y/n): ")
    if choice.lower() == 'y':
        webbrowser.open('https://vercel.com')

def show_all_options():
    """Show all deployment options"""
    print("\n📋 All Free Deployment Options:")
    print("\n🏆 Railway (Recommended):")
    print("   - $5 free credit monthly")
    print("   - Zero configuration")
    print("   - Auto-deploy from GitHub")
    print("   - Custom domains included")
    
    print("\n🥈 Render:")
    print("   - 750 free hours/month")
    print("   - Automatic HTTPS")
    print("   - Easy setup")
    
    print("\n🥉 Heroku:")
    print("   - Free tier available")
    print("   - Well-documented")
    print("   - Large community")
    
    print("\n🚀 Fly.io:")
    print("   - 3 free shared-cpu VMs")
    print("   - Global edge deployment")
    print("   - Great performance")
    
    print("\n▲ Vercel:")
    print("   - Unlimited free deployments")
    print("   - Global CDN")
    print("   - Automatic HTTPS")

def main():
    """Main deployment function"""
    print_banner()
    
    # Check prerequisites
    if not check_requirements():
        print("❌ Please ensure requirements.txt exists")
        return
    
    check_git_repo()
    
    while True:
        show_deployment_options()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            deploy_railway()
            break
        elif choice == '2':
            deploy_render()
            break
        elif choice == '3':
            deploy_heroku()
            break
        elif choice == '4':
            deploy_fly()
            break
        elif choice == '5':
            deploy_vercel()
            break
        elif choice == '6':
            show_all_options()
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
