SuperEarth Family Hub – Technical Architecture and Design
Overview
The SuperEarth Family Hub is a Windows-based Python application that uses Tkinter to present a family-friendly dashboard on a large TV or kiosk. It combines:

A shared Google Calendar agenda

Live Reolink NVR camera feeds

Software-Defined Radio (SDR) monitoring for weather, police, and emergency channels

ADS-B aircraft tracking

An interactive property map with user-placed notes

All heavy I/O tasks run in background threads, while Tkinter’s main thread updates the interface.

System Architecture
Layer	Responsibility	Key Technologies
UI Layer	Build and update all Tkinter widgets; coordinate modules	Tkinter, ttk, TkinterMapView
Service Modules	One per feature (Calendar, Camera, SDR, ADS-B, Map)	Google API client, OpenCV + Pillow, rtl_433, pyrtlsdr/SoapySDR, dump1090
Concurrency	Keep UI responsive; route data from worker threads to UI	threading, queue.Queue, root.after()
Config & Storage	Store credentials, URLs, map notes	JSON / INI files, optional KML for map export

Module Breakdown
1. Google Calendar Service
Auth & API – Use Google’s OAuth desktop flow and Calendar API (read-only scope).

Data Flow – Worker thread fetches upcoming events every N minutes → places list in a queue → main thread renders in a ttk.Treeview or Listbox.

Config – credentials.json (client ID/secret) and token.json (refresh token).

2. Reolink Camera Module
Capture – cv2.VideoCapture(rtsp_url) grabs frames; convert to PIL.Image → ImageTk.PhotoImage.

Threading – One thread per stream; latest frame shared with UI (queue or shared var).

Display – Large Label/Canvas at top of dashboard; optional controls for feed selection.

3. SDR Module
rtl_433 subprocess for 433 / 868 / 915 MHz sensor data (rtl_433 -F json).

Optional scanning – pyrtlsdr loop over NOAA/police frequencies; log when a signal crosses threshold.

Output – Worker thread parses JSON or frequency events → UI text log with timestamps.

4. ADS-B Aircraft Module
dump1090 runs in network mode on the ADS-B dongle.

Socket Reader Thread connects to localhost:30003, parses comma-separated messages, updates an in-memory aircraft table.

UI – A ttk.Treeview lists Flight / Altitude / Speed, refreshed every second.

5. Map & Notes Module
TkinterMapView with Google satellite tile server

python
Copy
Edit
map_widget.set_tile_server(
    "https://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}")
Center on Property – set_position(lat, lon, zoom=18) or set_address("123 Main St, USA").

Annotation Workflow

User clicks “Add Note” → toggles placement mode.

Next map click captures lat/lon → prompt for note text.

map_widget.set_marker(lat, lon, text=note).

Persistence – Save markers to markers.json (or export KML).

Concurrency Pattern
text
Copy
Edit
[Camera Thread] ─┐
[rtl_433 Thread] ─┤  →  Thread-safe Queue  →  Tkinter main thread (UI)
[ADS-B Thread] ───┘
Each worker thread never touches Tkinter directly.

Main thread polls queues via root.after(interval, poll_queues).

Shared data (e.g., aircraft dict) protected by threading.Lock.

Tkinter Layout (16:9 Screen)
java
Copy
Edit
┌───────────────────────────────┐
│        Camera Feed (40%)      │
├───────────────┬───────────────┬───────────────┤
│   Calendar    │     SDR Log   │   Aircraft    │
│               │               │               │
│               │               │               │
└───────────────┴───────────────┴───────────────┘
Camera Feed – big, centered, high-value.

Bottom Row – three equal frames:

Calendar agenda

Scrolling SDR events

Live aircraft list (or tabbed with Map)

Map View – opened full-screen in a separate Toplevel window when needed.

Styling & Usability
Use ttk themes or ttkbootstrap; set a dark background with high-contrast text.

Increase base font (e.g., 16 pt) for TV readability.

All buttons large enough for touch or remote pointer.

Run main window in full-screen (root.attributes('-fullscreen', True)); bind Esc to exit.

Example Pseudocode Skeleton
python
Copy
Edit
class SuperEarthHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SuperEarth Family Hub")
        self.state("zoomed")          # maximize
        self.create_frames()
        self.start_services()
        self.poll_queues()            # kick off UI update loop

    def create_frames(self):
        # top: camera
        self.cam_label = ttk.Label(self)
        self.cam_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        # bottom: calendar, sdr, aircraft
        self.calendar_view = ttk.Treeview(self, columns=("Date","Time","Event"))
        self.calendar_view.grid(row=1, column=0, sticky="nsew")
        self.sdr_log = tk.Text(self, state="disabled")
        self.sdr_log.grid(row=1, column=1, sticky="nsew")
        self.aircraft_view = ttk.Treeview(self, columns=("Flight","Alt","Spd"))
        self.aircraft_view.grid(row=1, column=2, sticky="nsew")
        # configure grid weights
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=3)
        for c in range(3):
            self.grid_columnconfigure(c, weight=1)

    def start_services(self):
        self.cam_service = CameraFeed(self.cam_label)
        self.cam_service.start()
        self.calendar_service = CalendarService()
        self.calendar_service.start()
        self.sdr_service = SDRService()
        self.sdr_service.start()
        self.adsb_service = ADSBService()
        self.adsb_service.start()

    def poll_queues(self):
        # drain queues from each module, update widgets
        # ...
        self.after(200, self.poll_queues)  # poll again
Future Enhancements
Plot ADS-B positions on the map in real time.

Support multiple camera thumbnails with click-to-enlarge.

Play audio from selected SDR channels.

Home-automation hooks (e.g., alert overlays when a sensor triggers).

Summary
This architecture cleanly separates each feature into its own service module, uses threads for all continuous I/O, and routes data safely to a Tkinter dashboard optimized for a large screen. By following the module outlines and concurrency model above, you can implement the SuperEarth Family Hub incrementally, testing each component in isolation before integrating them into the complete family-friendly interface.
