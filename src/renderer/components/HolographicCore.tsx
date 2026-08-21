import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface HolographicCoreProps {
  state: 'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING';
  audioLevel?: number;
}

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

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const width = container.clientWidth || 400;
    const height = container.clientHeight || 400;

    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Particle Sphere Geometry
    const particleCount = 1400;
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

      // Initial Cyan Tint
      colors[i * 3] = 0.0;
      colors[i * 3 + 1] = 0.94;
      colors[i * 3 + 2] = 1.0;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Particle Material
    const material = new THREE.PointsMaterial({
      size: 0.035,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Inner Glowing Wireframe Core
    const innerGeo = new THREE.IcosahedronGeometry(0.9, 2);
    const innerMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.25,
    });
    const innerCore = new THREE.Mesh(innerGeo, innerMat);
    scene.add(innerCore);

    // Outer Orbital Ring
    const ringGeo = new THREE.TorusGeometry(2.1, 0.015, 16, 100);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.35,
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / 3;
    scene.add(ring);

    // Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();
      const currentState = stateRef.current;
      const currentAudio = audioLevelRef.current;

      const pos = geometry.attributes.position.array as Float32Array;
      const col = geometry.attributes.color.array as Float32Array;

      let speedMultiplier = 1.0;
      let targetColor = { r: 0.0, g: 0.94, b: 1.0 }; // Cyan (Standby)

      if (currentState === 'LISTENING') {
        speedMultiplier = 1.4;
        targetColor = { r: 0.0, g: 1.0, b: 0.7 }; // Emerald/Cyan
      } else if (currentState === 'THINKING') {
        speedMultiplier = 3.2;
        targetColor = { r: 0.96, g: 0.62, b: 0.04 }; // Amber/Gold
      } else if (currentState === 'SPEAKING') {
        speedMultiplier = 2.0;
        targetColor = { r: 0.22, g: 0.74, b: 0.97 }; // Electric Sky
      }

      particles.rotation.y = time * 0.25 * speedMultiplier;
      particles.rotation.x = time * 0.15 * speedMultiplier;
      innerCore.rotation.y = -time * 0.4 * speedMultiplier;
      innerCore.rotation.z = time * 0.2 * speedMultiplier;
      ring.rotation.z = time * 0.3 * speedMultiplier;

      // Particle Displacement Dynamics
      for (let i = 0; i < particleCount; i++) {
        const ox = originalPositions[i * 3];
        const oy = originalPositions[i * 3 + 1];
        const oz = originalPositions[i * 3 + 2];

        let offset = 0;
        if (currentState === 'LISTENING') {
          offset = Math.sin(time * 6.0 + i) * (0.15 + currentAudio * 0.35);
        } else if (currentState === 'THINKING') {
          offset = Math.sin(time * 12.0 + ox * 3.0) * 0.25;
        } else if (currentState === 'SPEAKING') {
          offset = Math.sin(time * 8.0 + oz * 4.0) * 0.2;
        } else {
          offset = Math.sin(time * 1.5 + i * 0.1) * 0.04;
        }

        const scale = 1.0 + offset;
        pos[i * 3] = ox * scale;
        pos[i * 3 + 1] = oy * scale;
        pos[i * 3 + 2] = oz * scale;

        // Smooth Color Shift
        col[i * 3] += (targetColor.r - col[i * 3]) * 0.05;
        col[i * 3 + 1] += (targetColor.g - col[i * 3 + 1]) * 0.05;
        col[i * 3 + 2] += (targetColor.b - col[i * 3 + 2]) * 0.05;
      }

      geometry.attributes.position.needsUpdate = true;
      geometry.attributes.color.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const newWidth = container.clientWidth || 400;
      const newHeight = container.clientHeight || 400;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div className="relative w-full h-full flex items-center justify-center pointer-events-none">
      {/* Glow Center Flare */}
      <div
        className={`absolute w-72 h-72 rounded-full blur-3xl transition-all duration-700 ${
          state === 'LISTENING'
            ? 'bg-neon-emerald/20'
            : state === 'THINKING'
            ? 'bg-neon-amber/20'
            : state === 'SPEAKING'
            ? 'bg-neon-blue/25'
            : 'bg-neon-cyan/15'
        }`}
      />
      {/* 3D Canvas Mount Point */}
      <div ref={mountRef} className="w-full h-full" />
    </div>
  );
};
