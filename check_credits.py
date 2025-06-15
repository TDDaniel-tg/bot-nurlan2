#!/usr/bin/env python3
"""
Скрипт для проверки кредитов CloudConvert
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDCONVERT_API_KEY = os.getenv('CLOUDCONVERT_API_KEY')
CLOUDCONVERT_BASE_URL = 'https://api.cloudconvert.com/v2'

async def check_credits():
    """Проверка оставшихся кредитов CloudConvert"""
    if not CLOUDCONVERT_API_KEY:
        print("❌ CLOUDCONVERT_API_KEY не установлен!")
        return
    
    headers = {
        'Authorization': f'Bearer {CLOUDCONVERT_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Проверяем информацию об аккаунте
            async with session.get(f"{CLOUDCONVERT_BASE_URL}/users/me", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    credits = user_data['data'].get('credits', {})
                    
                    print("📊 Информация об аккаунте CloudConvert:")
                    print(f"📧 Email: {user_data['data'].get('email', 'N/A')}")
                    print(f"💰 Кредиты: {credits.get('used', 0)} / {credits.get('total', 0)} использовано")
                    print(f"🔋 Осталось: {credits.get('total', 0) - credits.get('used', 0)} кредитов")
                    
                    # Проверяем лимиты
                    limits = user_data['data'].get('limits', {})
                    if limits:
                        print("\n🔒 Лимиты аккаунта:")
                        for key, value in limits.items():
                            print(f"   {key}: {value}")
                    
                    # Показываем план
                    plan = user_data['data'].get('plan', {})
                    if plan:
                        print(f"\n📋 План: {plan.get('name', 'N/A')}")
                        if plan.get('expires_at'):
                            print(f"⏰ Истекает: {plan['expires_at']}")
                
                else:
                    error_text = await response.text()
                    print(f"❌ Ошибка получения информации: {response.status} - {error_text}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")

async def check_job_history(limit=5):
    """Проверка истории заданий"""
    if not CLOUDCONVERT_API_KEY:
        print("❌ CLOUDCONVERT_API_KEY не установлен!")
        return
    
    headers = {
        'Authorization': f'Bearer {CLOUDCONVERT_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{CLOUDCONVERT_BASE_URL}/jobs?per_page={limit}&sort=created_at", 
                headers=headers
            ) as response:
                if response.status == 200:
                    jobs_data = await response.json()
                    jobs = jobs_data['data']
                    
                    print(f"\n📋 Последние {len(jobs)} заданий:")
                    for job in jobs:
                        status_emoji = {
                            'finished': '✅',
                            'error': '❌', 
                            'processing': '🔄',
                            'waiting': '⏳'
                        }.get(job.get('status', ''), '❓')
                        
                        print(f"   {status_emoji} {job.get('id')}: {job.get('status')} ({job.get('created_at', '')})")
                        if job.get('message'):
                            print(f"      💬 {job['message']}")
                
                else:
                    error_text = await response.text()
                    print(f"❌ Ошибка получения истории: {response.status} - {error_text}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🔍 Проверка CloudConvert...")
    asyncio.run(check_credits())
    asyncio.run(check_job_history()) 