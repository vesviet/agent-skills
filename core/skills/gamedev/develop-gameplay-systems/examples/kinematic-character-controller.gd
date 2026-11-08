class_name KinematicCharacterController
extends CharacterBody3D

@export var move_speed: float = 6.0
@export var jump_impulse: float = 9.0
@export var gravity: float = 24.0
@export var acceleration: float = 40.0
@export var friction: float = 30.0

# State Machine definitions
enum State { IDLE, RUN, JUMP, FALL }
var current_state: State = State.IDLE

# Input Buffers & Coyote Time
var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
const COYOTE_DURATION: float = 0.12
const JUMP_BUFFER_DURATION: float = 0.15

func _physics_process(delta: float) -> void:
	# Update timers
	if is_on_floor():
		coyote_timer = COYOTE_DURATION
	else:
		coyote_timer = max(0.0, coyote_timer - delta)

	jump_buffer_timer = max(0.0, jump_buffer_timer - delta)

	# Read Input Actions
	var input_dir: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var move_vector: Vector3 = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if Input.is_action_just_pressed("jump"):
		jump_buffer_timer = JUMP_BUFFER_DURATION

	# State Transitions & Physics Integration
	match current_state:
		State.IDLE:
			apply_horizontal_velocity(Vector3.ZERO, friction, delta)
			if not is_on_floor() and coyote_timer <= 0.0:
				transition_to(State.FALL)
			elif jump_buffer_timer > 0.0 and coyote_timer > 0.0:
				execute_jump()
			elif move_vector.length_squared() > 0.01:
				transition_to(State.RUN)

		State.RUN:
			apply_horizontal_velocity(move_vector * move_speed, acceleration, delta)
			if not is_on_floor() and coyote_timer <= 0.0:
				transition_to(State.FALL)
			elif jump_buffer_timer > 0.0 and coyote_timer > 0.0:
				execute_jump()
			elif move_vector.length_squared() <= 0.01:
				transition_to(State.IDLE)

		State.JUMP:
			velocity.y -= gravity * delta
			apply_horizontal_velocity(move_vector * move_speed, acceleration * 0.5, delta)
			if velocity.y <= 0.0:
				transition_to(State.FALL)

		State.FALL:
			velocity.y -= gravity * delta
			apply_horizontal_velocity(move_vector * move_speed, acceleration * 0.5, delta)
			if is_on_floor():
				if move_vector.length_squared() > 0.01:
					transition_to(State.RUN)
				else:
					transition_to(State.IDLE)

	move_and_slide()

func transition_to(new_state: State) -> void:
	current_state = new_state

func execute_jump() -> void:
	velocity.y = jump_impulse
	coyote_timer = 0.0
	jump_buffer_timer = 0.0
	transition_to(State.JUMP)

func apply_horizontal_velocity(target_vel: Vector3, rate: float, delta: float) -> void:
	var h_vel: Vector3 = Vector3(velocity.x, 0, velocity.z)
	h_vel = h_vel.move_toward(target_vel, rate * delta)
	velocity.x = h_vel.x
	velocity.z = h_vel.z
