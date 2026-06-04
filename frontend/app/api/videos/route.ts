import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    const videosDir = path.join(process.cwd(), 'public', 'videos');
    if (!fs.existsSync(videosDir)) {
      return NextResponse.json({ videos: [] });
    }
    const files = fs.readdirSync(videosDir).filter(file => file.endsWith('.mp4'));
    return NextResponse.json({ videos: files });
  } catch (error) {
    return NextResponse.json({ videos: [] });
  }
}
