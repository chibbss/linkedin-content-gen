# linkedin-content-gen
<img width="1361" alt="Screenshot 2025-05-01 at 22 13 57" src="https://github.com/user-attachments/assets/09388293-9a21-487c-9cf2-279e67b968a2" />

<img width="854" alt="Screenshot 2025-05-01 at 22 01 12" src="https://github.com/user-attachments/assets/0e635e52-1289-466d-8221-7061fc92c7f4" />


📄 Project Summary: LinkedIn Post Generator Prototype

🧠 Objective

A lightweight MVP that:
	•	Accepts a CSV of viral LinkedIn posts (e.g., exported from PhantomBuster),
	•	Lets a user input product-related info and brand voice,
	•	Sends the data to an API to generate a new LinkedIn post,
	•	Displays the output cleanly,
	•	Provides download/upload options for the generated result.

⸻

⚙️ Tools & Technologies

Tool/Service	Purpose
Streamlit	UI frontend for quick prototyping
FastAPI	Backend API endpoint for post generation
Ngrok	Tunnel local backend to public web
Pandas	CSV handling and output formatting
Uploadcare	(Planned) Cloud-based upload and sharing
Google Drive (Make)	(Attempted) Cloud file upload



⸻

🛠️ Implementation Breakdown

1. Frontend - Streamlit App
	•	CSV upload form with optional preview.
	•	Input form with fields like topic, brand voice, mission, CTA, and optional viral reference metrics.
	•	POST request to localhost:8000/generate-final-post when form is submitted.
	•	Rendered results with:
	•	Display of generated post
	•	Contextual metadata
	•	Download option for result file (initially .csv, later updated to .txt)

2. Backend (Local FastAPI)
	•	Assumed to be running locally, with /generate-final-post accepting JSON payload.
	•	Returned response includes generated post, brand voice used, CTA link, and inspiration data.

⸻

🔁 File Handling (Final Output)

🔽 Download Option
	•	Originally implemented as downloadable .csv.
	•	Corrected to .txt after realizing CSV was not ideal for a single text post.

☁️ Upload Options Considered
	1.	Google Drive (via Make scenario)
	•	Issue: Restricted scopes not allowed for @gmail.com accounts.
	•	Blocked due to OAuth limitations with consumer Gmail accounts.
	2.	Uploadcare API (planned fallback)
	•	Lightweight API to handle uploads without OAuth.
	•	Simpler and frictionless for public link sharing.
	•	Was not implemented in final app but considered the most viable alternative.

⸻

❌ Bottlenecks & Challenges

Challenge	Notes
Ngrok tunnel instability	Required to expose FastAPI for external access; needed reauthentication and was inconsistent.
Google Drive OAuth restrictions	Couldn’t upload from a @gmail.com account due to restricted scopes to finalize the make scenario.
File type confusion	Post was initially downloadable as .csv, though .txt made more sense for the content.
Make Webhook Limitations	Webhook testing and custom endpoints caused delays.



⸻

✅ Outcome

Despite the roadblocks, you successfully:
	•	Prototyped a usable UI with Streamlit.
	•	Connected it to a working FastAPI backend.
	•	Accepted and parsed viral CSV data.
	•	Took user input and generated a customized post.
	•	Offered local download of the final result.

⸻

📌 Next Steps
	•	Implement Uploadcare for seamless file sharing (if cloud upload is still needed).
	•	Deploy backend to a public server (e.g., Render, Fly.io) to eliminate Ngrok dependency.
	•	Expand CSV parsing logic to support richer formats (e.g., multiple posts).
	•	Add image or media support for richer post creation.

⸻

Would you like this written up in a Google Doc or markdown file format?
