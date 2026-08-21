import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface AICoreSphereProps {
  isSpeaking?: boolean;
  state?: 'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING';
}

const COLOR_IDLE = new THREE.Color('#00f0ff');
const COLOR_ACTIVE = new THREE.Color('#10b981');
const COLOR_THINKING = new THREE.Color('#f59e0b');
const COLOR_SPEAKING = new THREE.Color('#38bdf8');
const _tempColor = new THREE.Color();

export const AICoreSphere: React.FC<AICoreSphereProps> = ({ isSpeaking = false, state = 'STANDBY' }) => {
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

    const width = container.clientWidth || 360;
    const height = container.clientHeight || 360;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.z = 3.5;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: false,
      powerPreference: 'default',
      precision: 'lowp',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(1.0);
    container.appendChild(renderer.domElement);

    const count = 400;
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const phi = Math.acos(1 - (2 * (i + 0.5)) / count);
      const theta = Math.PI * (1 + Math.sqrt(5)) * i;
      positions[i * 3] = 1.2 * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = 1.2 * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = 1.2 * Math.cos(phi);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      size: 0.025,
      color: COLOR_IDLE,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    let animationId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationId = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const speaking = isSpeakingRef.current;
      const st = stateRef.current;

      particles.rotation.y += delta * (speaking ? 0.35 : 0.08);
      particles.rotation.x += delta * 0.04;

      if (st === 'THINKING') {
        _tempColor.copy(COLOR_THINKING);
      } else if (st === 'SPEAKING' || speaking) {
        _tempColor.copy(COLOR_SPEAKING);
      } else if (st === 'LISTENING') {
        _tempColor.copy(COLOR_ACTIVE);
      } else {
        _tempColor.copy(COLOR_IDLE);
      }

      material.color.lerp(_tempColor, 0.08);
      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth || 360;
      const h = container.clientHeight || 360;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationId);
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
};

export default AICoreSphere;
