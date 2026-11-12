import math
from PIL import Image, ImageDraw, ImageFont

def make_cyber_icon(output_path, size=(900, 900)):
    # Create transparent image
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Center coordinates
    cx, cy = size[0] // 2, size[1] // 2

    # Draw cute glowing shield
    # Shield points
    w, h = 320, 380
    top_y = cy - h//2
    bot_y = cy + h//2
    left_x = cx - w//2
    right_x = cx + w//2

    # Outer soft glow / outline
    for offset, alpha, color in [(16, 40, (100, 180, 255)), (10, 80, (50, 140, 240)), (0, 255, (30, 110, 220))]:
        # Shield polygon
        points = [
            (cx, top_y - offset),
            (right_x + offset, top_y + 40),
            (right_x + offset - 20, cy + 60),
            (cx, bot_y + offset),
            (left_x - offset + 20, cy + 60),
            (left_x - offset, top_y + 40),
        ]
        draw.polygon(points, fill=color + (alpha,) if offset == 0 else (200, 230, 255, alpha))

    # Inner shield gradient fill
    inner_points = [
        (cx, top_y + 12),
        (right_x - 12, top_y + 45),
        (right_x - 30, cy + 50),
        (cx, bot_y - 12),
        (left_x + 30, cy + 50),
        (left_x + 12, top_y + 45),
    ]
    draw.polygon(inner_points, fill=(66, 153, 225, 255))

    # Inner highlight
    hl_points = [
        (cx, top_y + 20),
        (cx, bot_y - 25),
        (left_x + 35, cy + 45),
        (left_x + 20, top_y + 50),
    ]
    draw.polygon(hl_points, fill=(99, 179, 237, 255))

    # Draw cute golden lock in the center
    lock_cx, lock_cy = cx, cy + 10
    lock_w, lock_h = 160, 140

    # Shackle (the loop)
    shackle_bbox = (lock_cx - 50, lock_cy - 120, lock_cx + 50, lock_cy - 10)
    draw.arc(shackle_bbox, 180, 360, fill=(220, 225, 230), width=28)
    draw.arc(shackle_bbox, 180, 360, fill=(245, 247, 250), width=18)

    # Lock body (golden rounded rectangle)
    body_bbox = (lock_cx - lock_w//2, lock_cy - 20, lock_cx + lock_w//2, lock_cy + lock_h - 20)
    draw.rounded_rectangle(body_bbox, radius=28, fill=(246, 173, 85, 255), outline=(221, 107, 32, 255), width=8)

    # Cute face on the lock! (Cute smiling eyes and rosy cheeks)
    # Eyes (happy curved arcs)
    draw.arc((lock_cx - 45, lock_cy + 15, lock_cx - 15, lock_cy + 45), 200, 340, fill=(74, 85, 104, 255), width=7)
    draw.arc((lock_cx + 15, lock_cy + 15, lock_cx + 45, lock_cy + 45), 200, 340, fill=(74, 85, 104, 255), width=7)

    # Rosy cheeks
    draw.ellipse((lock_cx - 58, lock_cy + 38, lock_cx - 38, lock_cy + 54), fill=(254, 178, 178, 200))
    draw.ellipse((lock_cx + 38, lock_cy + 38, lock_cx + 58, lock_cy + 54), fill=(254, 178, 178, 200))

    # Smile
    draw.arc((lock_cx - 16, lock_cy + 32, lock_cx + 16, lock_cy + 58), 20, 160, fill=(74, 85, 104, 255), width=6)

    # Cute keyhole at bottom
    draw.ellipse((lock_cx - 10, lock_cy + 65, lock_cx + 10, lock_cy + 85), fill=(192, 86, 33, 255))
    draw.polygon([(lock_cx - 6, lock_cy + 75), (lock_cx + 6, lock_cy + 75), (lock_cx + 10, lock_cy + 98), (lock_cx - 10, lock_cy + 98)], fill=(192, 86, 33, 255))

    # Draw sparkling stars around
    def draw_star(sx, sy, rad, col):
        pts = []
        for i in range(8):
            r = rad if i % 2 == 0 else rad * 0.4
            angle = i * math.pi / 4
            pts.append((sx + r * math.cos(angle), sy + r * math.sin(angle)))
        draw.polygon(pts, fill=col)

    draw_star(cx - 210, cy - 120, 35, (255, 215, 0, 255))
    draw_star(cx + 200, cy - 140, 42, (255, 215, 0, 255))
    draw_star(cx + 220, cy + 130, 28, (99, 179, 237, 255))
    draw_star(cx - 190, cy + 140, 25, (254, 178, 178, 255))

    img.save(output_path, "PNG")
    print(f"Generated cute cyber icon at {output_path}")

make_cyber_icon(r"c:\2026AI_Agent\教學駕駛艙\cyber_shield.png")
