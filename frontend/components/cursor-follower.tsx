"use client";

import { useEffect, useState } from "react";

export function CursorFollower() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);

  useEffect(() => {
    const updateCursorPosition = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest("button") || target.closest("a") || target.closest(".hover-magnet")) {
        setIsHovering(true);
      } else {
        setIsHovering(false);
      }
    };

    window.addEventListener("mousemove", updateCursorPosition);
    window.addEventListener("mouseover", handleMouseOver);

    return () => {
      window.removeEventListener("mousemove", updateCursorPosition);
      window.removeEventListener("mouseover", handleMouseOver);
    };
  }, []);

  return (
    <>
      <div 
        className={`cursor-follower ${isHovering ? "scale-150 bg-primary/20" : "scale-100"}`}
        style={{ transform: `translate3d(${position.x - 16}px, ${position.y - 16}px, 0)` }}
      />
      <div 
        className={`cursor-glow ${isHovering ? "opacity-100 scale-110" : "opacity-0 scale-100"}`}
        style={{ transform: `translate3d(${position.x - 128}px, ${position.y - 128}px, 0)` }}
      />
    </>
  );
}
