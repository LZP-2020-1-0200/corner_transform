
import numpy as np


def transition_matrix(
		base_in_A_space_coordinates: np.ndarray, # [A, B, C]
		base_in_B_space_coordinates: np.ndarray, # [A, B, C]
	):
	"""Returns a transition matrix from A space to B space"""
	pass


def coords_to_base(arr):
	return np.array([
		[
			arr[1,0] - arr[0,0],
			arr[2,0] - arr[0,0],
			arr[0,0]
		],
		[
			arr[1,1] - arr[0,1],
			arr[2,1] - arr[0,1],
			arr[0,1]
		],
		[
			0, 0, 1
		]
	], dtype=np.float64)

def precalc_bases(
		base_in_A_space_coordinates: np.ndarray, # [A, B, C]
		base_in_B_space_coordinates: np.ndarray, # [A, B, C]
		base_in_transition_space_A_coordinates: np.ndarray, # [A, B, C]
		base_in_transition_space_B_coordinates: np.ndarray, # [A, B, C]
	):
	"""Returns a transition matrix from A space to B space"""
	# p_B = b_B @ p_b_B = b_B @ inverse(t_B) @ t_A @ p_b_A = b_B @ inverse(t_B) @ t_A @ inverse(b_A) @ p_A
	return base_in_B_space_coordinates @ np.linalg.inv(base_in_transition_space_B_coordinates) @ base_in_transition_space_A_coordinates @ np.linalg.inv(base_in_A_space_coordinates)

def calc_points(
		base_in_A_space_coordinates: np.ndarray, # [A, B, C]
		base_in_B_space_coordinates: np.ndarray, # [A, B, C]
		base_in_transition_space_A_coordinates: np.ndarray, # [A, B, C]
		base_in_transition_space_B_coordinates: np.ndarray, # [A, B, C]
		points_in_A_space_coordinates: np.ndarray, # list of points in A space
	):
	base_in_A_space_coordinates = coords_to_base(base_in_A_space_coordinates)
	base_in_B_space_coordinates = coords_to_base(base_in_B_space_coordinates)
	base_in_transition_space_A_coordinates = coords_to_base(base_in_transition_space_A_coordinates)
	base_in_transition_space_B_coordinates = coords_to_base(base_in_transition_space_B_coordinates)
	precalc = precalc_bases(
		base_in_A_space_coordinates,
		base_in_B_space_coordinates,
		base_in_transition_space_A_coordinates,
		base_in_transition_space_B_coordinates,
	)
	# turn all [x,y] into [x,y,1]
	points_in_A_space_coordinates = np.hstack((points_in_A_space_coordinates, np.ones((points_in_A_space_coordinates.shape[0], 1))))
	# p_B = precalc @ solve(b_A, p_A)
	
	
	return (precalc @ points_in_A_space_coordinates.T)[:2].reshape(-1)

if __name__ == "__main__":
	# different bases
	A_space_base = np.array([[0, 0], [0, 10], [10, 0]], dtype=np.float64)
	space_A_point = np.array([5, 5], dtype=np.float64)
	transition_space_base_A = np.array([[-2, 7], [5, 12], [1, 6]], dtype=np.float64)
	transition_space_base_B = np.array([[0, 0], [0, 10], [10, 0]], dtype=np.float64)
	B_space_base = np.array([[1, 1], [1, 12], [12, 1]], dtype=np.float64)
	# in B base, base_A_point should be (0.3, 0.9)
	# in B space, base_A_point should be (3.3, 9.9)
	base_B_point = calc_points(A_space_base, B_space_base, transition_space_base_A, transition_space_base_B, space_A_point.reshape(1,2))
	print(base_B_point)
	assert np.all(np.isclose(base_B_point,[4.3, 10.9]))#type: ignore
	# b_A - base in A space (given)
	# b_B - base in B space (given)
	# t_A - A base in transition space (given)
	# t_B - B base in transition space (given)
	# p_A - point in A space (given)
	# p_B - point in B space (needed)
	# p_t - point in transition space 
	# p_b_A - point in base in A space
	# p_b_B - point in base in B space

	# b_A @ p_b_A = p_A
	# p_b_A = inverse(b_A) @ p_A


	# p_b_A = solve(b_A, p_A)
	# p_t = t_A @ p_b_A
	# p_b_B = solve(t_B, p_t)
	# p_B = b_B @ p_b_B

	# t_A @ p_b_A = p_t
	# t_B @ p_b_B = p_t
	# t_A @ p_b_A = t_B @ p_b_B
	# p_b_B = inverse(t_B) @ t_A @ p_b_A
	# p_B = b_B @ p_b_B = b_B @ inverse(t_B) @ t_A @ p_b_A = b_B @ inverse(t_B) @ t_A @ inverse(b_A) @ p_A

	