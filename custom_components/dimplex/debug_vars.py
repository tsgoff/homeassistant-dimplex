import asyncio
import aiohttp
import json
import re

# This script helps find the correct variable IDs for your Dimplex heat pump.
# It will try a range of common IDs and show you which ones have data.

async def scan():
    print("Dimplex Variable Scanner")
    print("------------------------")
    username = input("Username (Email): ")
    password = input("Password: ")
    
    async with aiohttp.ClientSession() as session:
        # 1. Login
        print("\nLogging in...")
        # (Simplified login flow for the script)
        from api import login_with_credentials, get_devices, DimplexApiClient
        
        try:
            access_token, refresh_token = await login_with_credentials(username, password, session)
            print("Login successful!")
            
            # 2. Get Devices
            devices = await get_devices(access_token, session)
            if not devices:
                print("No devices found.")
                return
            
            device_id = list(devices.keys())[0]
            print(f"Found Device: {device_id} ({devices[device_id]['display_name']})")
            
            client = DimplexApiClient(device_id, access_token, refresh_token, session)
            
            # 3. Scan common ranges
            print("\nScanning common variable ranges (this may take a minute)...")
            
            # Ranges to check (based on typical Modbus mappings)
            ranges = [
                (1200, 1400), # Temperatures
                (1470, 1500), # Status
                (1600, 1650), # Targets
                (1720, 1730), # Energy old
                (1800, 1810), # Energy new
                (2170, 2180), # Heat quantity
                (2200, 2260), # Ventilation
                (2510, 2520), # Energy total candidates
            ]
            
            all_ids = []
            for start, end in ranges:
                all_ids.extend([f"{i}i" for i in range(start, end)])
                all_ids.extend([f"{i}a" for i in range(start, end)])
            
            # Fetch in chunks
            chunk_size = 50
            results = {}
            for i in range(0, len(all_ids), chunk_size):
                chunk = all_ids[i:i+chunk_size]
                try:
                    data = await client.get_variables(chunk)
                    for var in data:
                        if var.get("value") is not None:
                            results[var["variableCode"]] = var["value"]
                except Exception as e:
                    print(f"Error fetching chunk: {e}")

            print("\nActive Variables Found:")
            print("-----------------------")
            for code in sorted(results.keys()):
                print(f"ID: {code:<6} | Value: {results[code]}")
            
            print("\nScan complete. Compare these values with your Dimplex app to find energy IDs.")
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(scan())
