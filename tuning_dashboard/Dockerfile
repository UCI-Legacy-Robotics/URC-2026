FROM ros:humble-ros-base

# Shared libraries PyQt6's Qt binaries need to even import, let alone
# run -- ros:humble-ros-base is a minimal image with none of this.
# Xvfb/x11vnc/noVNC (the actual virtual display) are added in a later
# step; this is just what's needed for PyQt6 itself to load.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip \
        libgl1 \
        libegl1 \
        libxkbcommon0 \
        libxkbcommon-x11-0 \
        libdbus-1-3 \
        libnss3 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libxi6 \
        libxtst6 \
        libasound2 \
        fontconfig \
        libfreetype6 \
        libx11-xcb1 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Real entrypoint; a later step swaps this for a script that starts the
# virtual display (Xvfb/x11vnc/noVNC) before exec'ing this same command.
CMD ["python3", "main.py"]
