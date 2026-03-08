# YouTube Video/MP3 Downloader - SPEC.md

## 1. Project Overview

- **Project Name**: YouTube Downloader Pro
- **Type**: Web Application (Flask)
- **Core Functionality**: Download YouTube videos and MP3 audio from URL links
- **Target Users**: Users who want to download YouTube content for offline use

## 2. UI/UX Specification

### Layout Structure

- **Header**: Fixed top bar with logo and title
- **Hero Section**: Main content area with input form (centered)
- **Results Section**: Video info and download options (appears after URL submission)
- **Footer**: Simple footer with credits

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Visual Design

#### Color Palette
- **Background Base**: `#0a0a0f` (deep dark blue-black)
- **Primary**: `#00f0ff` (cyan neon)
- **Secondary**: `#ff00aa` (magenta neon)
- **Accent**: `#00ff88` (green neon)
- **Text Primary**: `#ffffff`
- **Text Secondary**: `#a0a0b0`
- **Card Background**: `rgba(20, 20, 40, 0.8)`

#### Typography
- **Font Family**: 'Orbitron' (headers), 'Exo 2' (body)
- **Title Size**: 3rem (desktop), 2rem (mobile)
- **Body Size**: 1rem
- **Font Weight**: 300-700

#### Visual Effects - Exaggerated Tech Style
1. **Animated Background**:
   - Multiple floating particles/spheres with glow
   - Moving grid lines (perspective effect)
   - Gradient waves that move across screen
   - Color: cyan and magenta particles with blur trails

2. **Glow Effects**:
   - Input fields: cyan outer glow on focus
   - Buttons: gradient glow (cyan to magenta)
   - Cards: subtle neon border glow

3. **Animations**:
   - Pulsing neon borders
   - Floating animation on particles
   - Fade-in/slide-up for results
   - Button hover: scale + intensified glow
   - Scanline overlay effect (subtle)

### Components

#### Input Form
- Large URL input with neon border
- Placeholder: "Paste YouTube URL here..."
- Submit button with gradient and glow
- Loading state with animated spinner

#### Video Preview Card
- Thumbnail image (if available)
- Video title
- Duration
- Format options (MP4, MP3)
- Quality selector (for video)
- Download button per format

#### Download Buttons
- Primary: Cyan gradient with glow
- Hover: Intensified glow + slight scale
- Active: Pressed effect
- Loading: Animated border

## 3. Functionality Specification

### Core Features
1. **URL Input**: Accept YouTube URL (various formats supported)
2. **Video Info Fetch**: Extract video title, thumbnail, duration
3. **Format Selection**: Choose MP4 (video) or MP3 (audio)
4. **Quality Selection**: For video - 1080p, 720p, 480p, 360p
5. **Download**: Serve file for download
6. **Error Handling**: Display user-friendly error messages

### User Flow
1. User pastes YouTube URL
2. Click "Process" button
3. App fetches video info and displays preview
4. User selects format and quality
5. Click download button
6. File downloads to user's device

### Backend (Flask)
- Route `/`: Main page
- Route `/process`: POST - Process URL, return video info
- Route `/download`: POST - Download the file
- Use `yt-dlp` library for YouTube extraction
- Temporary files cleaned up after download

### Edge Cases
- Invalid URL format
- Video unavailable/private
- Network errors
- Unsupported format
- Very long videos

## 4. Acceptance Criteria

- [ ] Page loads with animated tech background
- [ ] Input field accepts YouTube URLs
- [ ] Video info displays after processing
- [ ] MP3 and MP4 format options available
- [ ] Quality selection works for video
- [ ] Download initiates correctly
- [ ] Responsive on mobile, tablet, desktop
- [ ] All animations smooth (60fps)
- [ ] Error messages display properly
- [ ] Glow and neon effects visible
