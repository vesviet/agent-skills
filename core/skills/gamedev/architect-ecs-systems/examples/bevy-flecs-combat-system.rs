// Bevy ECS Combat & Movement System (2026)
// Demonstrates POD components, disjoint mutable queries, and deferred commands.

use bevy::prelude::*;

// Plain Old Data (POD) Components - Zero Heap Allocations
#[derive(Component, Debug, Clone, Copy)]
pub struct Position {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[derive(Component, Debug, Clone, Copy)]
pub struct Velocity {
    pub dx: f32,
    pub dy: f32,
    pub dz: f32,
}

#[derive(Component, Debug, Clone, Copy)]
pub struct Health {
    pub current: f32,
    pub max: f32,
}

#[derive(Component, Debug, Clone, Copy)]
pub struct Damage(pub f32);

#[derive(Component)]
pub struct Player;

#[derive(Component)]
pub struct Enemy;

// System 1: Kinematic Movement Integration (Read-Only Velocity, Mutable Position)
pub fn movement_system(time: Res<Time>, mut query: Query<(&Velocity, &mut Position)>) {
    let delta = time.delta_secs();
    for (vel, mut pos) in query.iter_mut() {
        pos.x += vel.dx * delta;
        pos.y += vel.dy * delta;
        pos.z += vel.dz * delta;
    }
}

// System 2: Combat Damage & Deferred Despawn (Disjoint Borrow from Movement)
pub fn combat_damage_system(
    mut commands: Commands,
    mut targets: Query<(Entity, &mut Health, &Damage)>,
) {
    for (entity, mut health, damage) in targets.iter_mut() {
        health.current -= damage.0;
        if health.current <= 0.0 {
            // Deferred structural mutation: record despawn into Command Buffer
            commands.entity(entity).despawn();
        }
    }
}

// System 3: Schedule Setup with Deterministic Pipeline Stages
pub struct GameplayPlugin;

impl Plugin for GameplayPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            (
                movement_system,
                combat_damage_system,
            ).chain(), // Deterministic sequential chaining or automatic parallel scheduling
        );
    }
}
