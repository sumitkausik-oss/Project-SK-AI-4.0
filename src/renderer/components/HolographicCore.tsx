import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface HolographicCoreProps {
  state: 'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING';
  audioLevel?: number;
}

// Pre-allocated static color objects outside the render loop to eliminate RAM garbage collection
const COLOR_STANDBY = { r: 0.0, g: 0.94, b: 1.0 }; // Cyan
const COLOR_LISTENING = { r: 0.0, g: 1.0, b: 0.7 }; // Neon Emerald
const COLOR_THINKING = { r: 0.96, g: 0.62, b: 0.04 }; // Gold / Amber
const COLOR_SPEAKING = { r: 0.22, g: 0.74, b: 0.97 }; // Electric Sky

export const HolographicCore: React.FC<HolographicCoreProps> = ({ state, audioLevel = 0 }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const stateRef = useRef(state);
  const audioLevelRef = useRef(audioLevel);

  useEffect(() => {
    stateRef.current = state;
    audioLevelRef.current = audioLevel;
  }, [state, audioLevel]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // 1. Optimized WebGLRenderer with lowp precision and capped DPR to minimize RAM & GPU load
    const width = container.clientWidth || 380;
    const height = container.clientHeight || 380;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'default',
      precision: 'lowp',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.25));
    container.appendChild(renderer.domElement);

    // 2. Particle Geometry Allocation
    const particleCount = 1200;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const originalPositions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const radius = 1.6;
    for (let i = 0; i < particleCount; i++) {
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = Math.cbrt(Math.random()) * 0.15 + radius;

      const sinPhi = Math.sin(phi);
      const x = r * sinPhi * Math.cos(theta);
      const y = r * sinPhi * Math.sin(theta);
      const z = r * Math.cos(phi);

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      originalPositions[i * 3] = x;
      originalPositions[i * 3 + 1] = y;
      originalPositions[i * 3 + 2] = z;

      colors[i * 3] = COLOR_STANDBY.r;
      colors[i * 3 + 1] = COLOR_STANDBY.g;
      colors[i * 3 + 2] = COLOR_STANDBY.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.032,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // 3. Inner Wireframe Core & Outer Torus
    const innerGeo = new THREE.IcosahedronGeometry(0.85, 2);
    const innerMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.22,
    });
    const innerCore = new THREE.Mesh(innerGeo, innerMat);
    scene.add(innerCore);

    const ringGeo = new THREE.TorusGeometry(2.0, 0.012, 12, 80);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.3,
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / 3;
    scene.add(ring);

    // 4. Animation Loop with Zero Per-Frame Allocations
    let animationFrameId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();
      const currentState = stateRef.current;
      const currentAudio = audioLevelRef.current;

      const pos = geometry.attributes.position.array as Float32Array;
      const col = geometry.attributes.color.array as Float32Array;

      let speedMultiplier = 1.0;
      let target = COLOR_STANDBY;

      if (currentState === 'LISTENING') {
        speedMultiplier = 1.4;
        target = COLOR_LISTENING;
      } else if (currentState === 'THINKING') {
        speedMultiplier = 3.0;
        target = COLOR_THINKING;
      } else if (currentState === 'SPEAKING') {
        speedMultiplier = 2.0;
        target = COLOR_SPEAKING;
      }

      particles.rotation.y = time * 0.22 * speedMultiplier;
      particles.rotation.x = time * 0.12 * speedMultiplier;
      innerCore.rotation.y = -time * 0.35 * speedMultiplier;
      ring.rotation.z = time * 0.25 * speedMultiplier;

      // In-place float buffer calculations without allocating objects
      for (let i = 0; i < particleCount; i++) {
        const ox = originalPositions[i * 3];
        const oy = originalPositions[i * 3 + 1];
        const oz = originalPositions[i * 3 + 2];

        let offset = 0;
        if (currentState === 'LISTENING') {
          offset = Math.sin(time * 6.0 + i) * (0.12 + currentAudio * 0.35);
        } else if (currentState === 'THINKING') {
          offset = Math.sin(time * 12.0 + ox * 3.0) * 0.22;
        } else if (currentState === 'SPEAKING') {
          offset = Math.sin(time * 8.0 + oz * 4.0) * 0.18;
        } else {
          offset = Math.sin(time * 1.5 + i * 0.1) * 0.035;
        }

        const scale = 1.0 + offset;
        pos[i * 3] = ox * scale;
        pos[i * 3 + 1] = oy * scale;
        pos[i * 3 + 2] = oz * scale;

        col[i * 3] += (target.r - col[i * 3]) * 0.06;
        col[i * 3 + 1] += (target.g - col[i * 3 + 1]) * 0.06;
        col[i * 3 + 2] += (target.b - col[i * 3 + 2]) * 0.06;
      }

      geometry.attributes.position.needsUpdate = true;
      geometry.attributes.color.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth || 380;
      const h = container.clientHeight || 380;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);

      // Clean disposal to eliminate memory leaks
      geometry.dispose();
      material.dispose();
      innerGeo.dispose();
      innerMat.dispose();
      ringGeo.dispose();
      ringMat.dispose();
      renderer.dispose();

      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div className="relative w-full h-full flex items-center justify-center pointer-events-none">
      <div
        className={`absolute w-64 h-64 rounded-full blur-3xl transition-all duration-700 ${
          state === 'LISTENING'
            ? 'bg-neon-emerald/20'
            : state === 'THINKING'
            ? 'bg-neon-amber/20'
            : state === 'SPEAKING'
            ? 'bg-neon-blue/25'
            : 'bg-neon-cyan/15'
        }`}
      />
      <div ref={mountRef} className="w-full h-full" />
    </div>
  );
};
