import struct
import zlib
import os

print("Generating Searchify Favicon Assets...")

# 1. Generate favicon.svg (Vector SVG for all modern browsers)
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="searchifyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2D62BF"/>
      <stop offset="45%" stop-color="#224D95"/>
      <stop offset="100%" stop-color="#16376E"/>
    </linearGradient>
  </defs>
  <!-- Searchify Signature Brand Mark Box (Matching .brand-mark) -->
  <rect x="2" y="2" width="60" height="60" rx="19" fill="url(#searchifyGrad)"/>
  <rect x="2" y="2" width="60" height="60" rx="19" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="1.5"/>
  <!-- Bold Centered 'S' -->
  <text x="32" y="34.5" font-family="-apple-system, BlinkMacSystemFont, 'Bricolage Grotesque', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="39" font-weight="900" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">S</text>
  <!-- Vibrant Pink Algorithm Spark Dot -->
  <circle cx="48" cy="16" r="4.5" fill="#D93D81"/>
  <circle cx="48" cy="16" r="1.8" fill="#FFFFFF"/>
</svg>"""

with open("favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"  [OK] Created favicon.svg ({len(svg_content)} bytes)")

# 2. Pure Python Supersampled PNG Renderer
def encode_png(width, height, pixel_data):
    raw = bytearray()
    for y in range(height):
        raw.append(0) # filter type 0: None
        for x in range(width):
            r, g, b, a = pixel_data[y][x]
            raw.extend([r, g, b, a])
    
    compressed = zlib.compress(raw, 9)
    
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    png.extend(struct.pack('>I', len(ihdr_data)))
    png.extend(b'IHDR')
    png.extend(ihdr_data)
    png.extend(struct.pack('>I', ihdr_crc))
    
    # IDAT
    idat_crc = zlib.crc32(b'IDAT' + compressed)
    png.extend(struct.pack('>I', len(compressed)))
    png.extend(b'IDAT')
    png.extend(compressed)
    png.extend(struct.pack('>I', idat_crc))
    
    # IEND
    iend_crc = zlib.crc32(b'IEND')
    png.extend(struct.pack('>I', 0))
    png.extend(b'IEND')
    png.extend(struct.pack('>I', iend_crc))
    
    return bytes(png)

def render_searchify_icon(size, sample_rate=4):
    sw = size * sample_rate
    sh = size * sample_rate
    
    r = int(sw * 0.30) # corner radius (matches 19/64)
    pad = int(sw * 0.035)
    x0, y0 = pad, pad
    x1, y1 = sw - pad, sh - pad
    
    # High-resolution S glyph pattern (16 rows x 14 cols)
    s_pattern = [
        '  ##########  ',
        ' ############ ',
        '###        ###',
        '###        ###',
        '###           ',
        ' ####         ',
        '  #########   ',
        '   ########## ',
        '     #########',
        '       #######',
        '           ###',
        '           ###',
        '###        ###',
        '###        ###',
        ' ############ ',
        '  ##########  '
    ]
    p_h = len(s_pattern)
    p_w = len(s_pattern[0])
    
    s_h = int(sh * 0.60)
    s_w = int(sw * 0.48)
    s_x0 = (sw - s_w) // 2
    s_y0 = (sh - s_h) // 2 + int(sh * 0.015)
    
    dot_cx = int(sw * 0.75)
    dot_cy = int(sh * 0.25)
    dot_r = int(sw * 0.07)
    
    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            r_acc, g_acc, b_acc, a_acc = 0, 0, 0, 0
            for sy in range(sample_rate):
                py = y * sample_rate + sy
                for sx in range(sample_rate):
                    px = x * sample_rate + sx
                    
                    # Rounded rectangle hit-test
                    inside_rect = False
                    if x0 <= px < x1 and y0 <= py < y1:
                        cx_b = x0 + r if px < x0 + r else (x1 - 1 - r if px >= x1 - r else px)
                        cy_b = y0 + r if py < y0 + r else (y1 - 1 - r if py >= y1 - r else py)
                        if (px - cx_b)**2 + (py - cy_b)**2 <= r**2:
                            inside_rect = True
                    
                    if not inside_rect:
                        continue
                    
                    # Subtle gradient from #2D62BF (45, 98, 191) to #16376E (22, 55, 110)
                    t = py / sh
                    bg_r = int(45 * (1 - t) + 22 * t)
                    bg_g = int(98 * (1 - t) + 55 * t)
                    bg_b = int(191 * (1 - t) + 110 * t)
                    
                    # Check S glyph
                    in_s = False
                    if s_x0 <= px < s_x0 + s_w and s_y0 <= py < s_y0 + s_h:
                        gx = int((px - s_x0) / s_w * p_w)
                        gy = int((py - s_y0) / s_h * p_h)
                        if 0 <= gy < p_h and 0 <= gx < p_w and s_pattern[gy][gx] == '#':
                            in_s = True
                    
                    # Check algorithm spark dot (#D93D81 with white core)
                    in_dot = False
                    in_dot_core = False
                    d_sq = (px - dot_cx)**2 + (py - dot_cy)**2
                    if d_sq <= dot_r**2:
                        in_dot = True
                        if d_sq <= (dot_r * 0.4)**2:
                            in_dot_core = True
                    
                    if in_dot_core:
                        r_acc += 255; g_acc += 255; b_acc += 255; a_acc += 255
                    elif in_dot:
                        r_acc += 217; g_acc += 61; b_acc += 129; a_acc += 255
                    elif in_s:
                        r_acc += 255; g_acc += 255; b_acc += 255; a_acc += 255
                    else:
                        r_acc += bg_r; g_acc += bg_g; b_acc += bg_b; a_acc += 255
            
            n = sample_rate * sample_rate
            row.append((r_acc // n, g_acc // n, b_acc // n, a_acc // n))
        pixels.append(row)
    
    return encode_png(size, size, pixels)

# Generate raster sizes
png_16 = render_searchify_icon(16, sample_rate=4)
with open("favicon-16x16.png", "wb") as f:
    f.write(png_16)
print(f"  [OK] Created favicon-16x16.png ({len(png_16)} bytes)")

png_32 = render_searchify_icon(32, sample_rate=4)
with open("favicon-32x32.png", "wb") as f:
    f.write(png_32)
print(f"  [OK] Created favicon-32x32.png ({len(png_32)} bytes)")

png_180 = render_searchify_icon(180, sample_rate=2)
with open("apple-touch-icon.png", "wb") as f:
    f.write(png_180)
print(f"  [OK] Created apple-touch-icon.png ({len(png_180)} bytes)")

png_192 = render_searchify_icon(192, sample_rate=2)
with open("favicon-192x192.png", "wb") as f:
    f.write(png_192)
print(f"  [OK] Created favicon-192x192.png ({len(png_192)} bytes)")

# 3. Generate standard favicon.ico (containing 32x32 and 16x16 icons)
ico = bytearray()
ico.extend(struct.pack('<HHH', 0, 1, 2)) # 2 images
offset = 6 + (16 * 2)

# Directory entry 1: 32x32
ico.extend(struct.pack('<BBBBHHII', 32, 32, 0, 0, 1, 32, len(png_32), offset))
offset += len(png_32)

# Directory entry 2: 16x16
ico.extend(struct.pack('<BBBBHHII', 16, 16, 0, 0, 1, 32, len(png_16), offset))

# Image payloads
ico.extend(png_32)
ico.extend(png_16)

with open("favicon.ico", "wb") as f:
    f.write(ico)
print(f"  [OK] Created favicon.ico ({len(ico)} bytes)")

print("\nAll Searchify favicon assets generated successfully!")
