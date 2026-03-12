import pygame
import math

def resolve_collision(ent1, ent2, sound_manager=None):
    # Distance between centers
    dist = ent1.pos.distance_to(ent2.pos)
    min_dist = ent1.radius + ent2.radius
    
    if dist < min_dist and dist > 0:
        # Collision detected
        if sound_manager:
            # Play player hit sound if at least one is a player, otherwise wall (approximation)
            sound_manager.play('hit_player')
            
        # Normal vector
        normal = (ent2.pos - ent1.pos).normalize()
        
        # Resolve overlap
        overlap = min_dist - dist
        # Distribute overlap correction based on mobility (usually 50/50 for buttons)
        ent1.pos -= normal * (overlap * 0.5)
        ent2.pos += normal * (overlap * 0.5)
        
        # Velocity reflection/transfer (Project velocities onto normal)
        v1n = ent1.vel.dot(normal)
        v2n = ent2.vel.dot(normal)
        
        # Elastic collision formulas
        restitution = 0.8
        
        # Assuming equal mass for all entities for simplicity 
        # (Ball is smaller but we want it to be pushed easily)
        new_v1n = v2n * restitution
        new_v2n = v1n * restitution
        
        ent1.vel += normal * (new_v1n - v1n)
        ent2.vel += normal * (new_v2n - v2n)

def check_all_collisions(entities, ball, sound_manager=None):
    # 1. Collisions between players
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            resolve_collision(entities[i], entities[j], sound_manager)
    
    # 2. Collisions between players and ball
    for ent in entities:
        resolve_collision(ent, ball, sound_manager)
