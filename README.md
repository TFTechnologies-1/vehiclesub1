# KARMALabs RTO Dashboard

Simple Flask app (KARMALabs-branded) to fetch RC info and challans from the RapidAPI "RTO Vehicle Information India" provider.

## Quick start (local)
1. Copy the files or download the zip.
2. Create a `.env` file from `.env.example` and add your RapidAPI key:
   ```
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```
3. Install deps:
   ```
   pip install -r requirements.txt
   ```
4. Run:
   ```
   python app.py
   ```
5. Open `http://127.0.0.1:5000`

## Deploy to Render
1. Create a new Web Service on Render and connect your GitHub repo.
2. Set the Environment Variable `RAPIDAPI_KEY` in Render (do NOT commit your key).
3. Render will detect `requirements.txt` and run `web: python app.py` from `Procfile`.

## Notes
- The app tries to call the documented `getVehicleInfo` endpoint for RC data.
- For challans it will try a few common endpoints; if you see empty results, let me know the exact challan endpoint from RapidAPI and I will update the app.
- Masked fields (owner/chassis) are controlled by the API provider and cannot be unmasked from the app.
