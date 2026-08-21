/**
 * SKAI — Quantum 3D AI Core Sphere (Pure Three.js Zero-Allocation Edition)
 * Product: SKAI Platform | Powered by SK Enterprises
 * Lead Architect: Sumeet Kumar | Version: 4.1.0
 */
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface AICoreSphereProps {
  isSpeaking?: boolean;
  state?: 'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING';
}

const COLOR_CYAN = { r: 0.0, g: 0.94, b: 1.0 };
const COLOR_EMERALD = { r: 0.06, g: 0.72, b: 0.5 };
const COLOR_AMBER = { r: 0.96, g: 0.62, b: 0.04 };

export default function AICoreSphere({ isSpeaking = false, state = 'STANDBY' }: AICoreSphereProps) {
  const mountRef = useRef<HTMLDivElement>(null);
  const isSpeakingRef = useRef(isSpeaking);
  const stateRef = useRef(state);

  useEffect(() => {
    isSpeakingRef.current = isSpeaking;
    stateRef.current = state;
  }, [isSpeaking, state]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 320;
    const height = container.clientHeight || 320;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 50);
    camera.position.z = 3.5;

    const renderer = new THREE.WebGLRenderer({
      antialias: false,
      alpha: true,
      powerPreference: 'default',
      precision: 'lowp',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.2));
    container.appendChild(renderer.domElement);

    const count = 450;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const phi = Math.acos(1 - (2 * (i + 0.5)) / count);
      const theta = Math.PI * (1 + Math.sqrt(5)) * i;
      positions[i * 3] = 1.25 * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = 1.25 * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = 1.25 * Math.cos(phi);

      colors[i * 3] = COLOR_CYAN.r;
      colors[i * 3 + 1] = COLOR_CYAN.g;
      colors[i * 3 + 2] = COLOR_CYAN.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.024,
      vertexColors: true,
      transparent: true,
      opacity: 0.88,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const points = new THREE.Points(geometry, material);
    scene.add(points);

    let animationFrameId: number;
    let lastTime = performance.now();

    const animate = (currentTime: number) => {
      animationFrameId = requestAnimationFrame(animate);
      const delta = Math.min((currentTime - lastTime) / 1000, 0.1);
      lastTime = currentTime;

      const speaking = isSpeakingRef.current || stateRef.current === 'SPEAKING';
      points.rotation.y += delta * (speaking ? 0.4 : 0.08);
      points.rotation.z += delta * 0.03;

      const col = geometry.attributes.color.array as Float32Array;
      const target = speaking ? COLOR_EMERALD : stateRef.current === 'THINKING' ? COLOR_AMBER : COLOR_CYAN;

      for (let i = 0; i < count; i++) {
        col[i * 3] += (target.r - col[i * 3]) * 0.08;
        col[i * 3 + 1] += (target.g - col[i * 3 + 1]) * 0.08;
        col[i * 3 + 2] += (target.b - col[i * 3 + 2]) * 0.08;
      }
      geometry.attributes.color.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animationFrameId = requestAnimationFrame(animate);

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth || 320;
      const h = container.clientHeight || 320;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div className="relative w-full h-full flex items-center justify-center pointer-events-none">
      <div ref={mountRef} className="w-full h-full" />
    </div>
  );
}
export { AICoreSphere };
