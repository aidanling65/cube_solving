import numpy as np
from .cube_strings import pad

def X_swap(num_str):
  return int(num_str[1] + num_str[0] + num_str[2:])

#swap to Z
def Z_swap(num_str):
  return int(num_str[2] + num_str[1] + num_str[0] + num_str[3:])

#change to y
def Y_swap(num_str):
  return int(num_str[0] + num_str[2] + num_str[1] + num_str[3:])

def X_prime(cube):
  reversed = cube[::-1, :, :]
  transposed = np.einsum('ijk...->jik...', reversed)
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(transposed)
  vector_X_swap = np.vectorize(X_swap)
  swapped = vector_X_swap(padded)
  return swapped

def X(cube):
  reversed = cube[:, ::-1, :]
  transposed = np.einsum('ijk...->jik...', reversed)
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(transposed)
  vector_X_swap = np.vectorize(X_swap)
  swapped = vector_X_swap(padded)
  return swapped

#change to z
def Z_prime(cube):
  reversed = cube[:, :, ::-1]
  transposed = np.einsum('ijk->kji', reversed)
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(transposed)
  vector_Z_swap = np.vectorize(Z_swap)
  swapped = vector_Z_swap(padded)
  return swapped

#change to z
def Z(cube):
  reversed = cube[::-1, :, :]
  transposed = np.einsum('ijk...->kji...', reversed)
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(transposed)
  vector_Z_swap = np.vectorize(Z_swap)
  swapped = vector_Z_swap(padded)
  return swapped

#change to y
def Y(cube):
  reversed = cube[:, ::-1, :]
  transposed = np.einsum('ijk...->ikj...', reversed)
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(transposed)
  vector_Y_swap = np.vectorize(Y_swap)
  swapped = vector_Y_swap(padded)
  return swapped

#change to y
def Y_prime(cube):
  reversed = cube[:, :, ::-1]
  transposed = np.einsum('ijk...->ikj...', reversed)
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(transposed)
  vector_Y_swap = np.vectorize(Y_swap)
  swapped = vector_Y_swap(padded)
  return swapped

def L(cube):
  left_slab = cube[:,:,0:1]
  left_slab = X_prime(left_slab)
  middle_slab = cube[:,:,1:2]
  right_slab = cube[:,:,2:]
  joined = np.concatenate([middle_slab, right_slab], axis=2)
  return np.concatenate([left_slab, joined], axis=2)

def L_prime(cube):
  left_slab = cube[:,:,0:1]
  left_slab = X(left_slab)
  middle_slab = cube[:,:,1:2]
  right_slab = cube[:,:,2:]
  joined = np.concatenate([middle_slab, right_slab], axis=2)
  return np.concatenate([left_slab, joined], axis=2)

def M(cube):
  left_slab = cube[:,:,0:1]
  middle_slab = cube[:,:,1:2]
  middle_slab = X_prime(middle_slab)
  right_slab = cube[:,:,2:]
  joined = np.concatenate([middle_slab, right_slab], axis=2)
  return np.concatenate([left_slab, joined], axis=2)

def M_prime(cube):
  left_slab = cube[:,:,0:1]
  middle_slab = cube[:,:,1:2]
  middle_slab = X(middle_slab)
  right_slab = cube[:,:,2:]
  joined = np.concatenate([middle_slab, right_slab], axis=2)
  return np.concatenate([left_slab, joined], axis=2)

def R_prime(cube):
  left_slab = cube[:,:,0:1]
  middle_slab = cube[:,:,1:2]
  right_slab = cube[:,:,2:]
  right_slab = X_prime(right_slab)
  joined = np.concatenate([middle_slab, right_slab], axis=2)
  return np.concatenate([left_slab, joined], axis=2)

def R(cube):
  left_slab = cube[:,:,0:1]
  middle_slab = cube[:,:,1:2]
  right_slab = cube[:,:,2:]
  right_slab = X(right_slab)
  joined = np.concatenate([middle_slab, right_slab], axis=2)
  return np.concatenate([left_slab, joined], axis=2)

#change to z
def B(cube):
  front_slab = cube[:,0:1,:]
  front_slab = Z_prime(front_slab)
  middle_slab = cube[:,1:2,:]
  back_slab = cube[:,2:,:]
  joined = np.concatenate([middle_slab, back_slab], axis=1)
  return np.concatenate([front_slab, joined], axis=1)

#change to z
def B_prime(cube):
  front_slab = cube[:,0:1,:]
  front_slab = Z(front_slab)
  middle_slab = cube[:,1:2,:]
  back_slab = cube[:,2:,:]
  joined = np.concatenate([middle_slab, back_slab], axis=1)
  return np.concatenate([front_slab, joined], axis=1)

#change to z
def S_prime(cube):
  front_slab = cube[:,0:1,:]
  middle_slab = cube[:,1:2,:]
  middle_slab = Z_prime(middle_slab)
  back_slab = cube[:,2:,:]
  joined = np.concatenate([middle_slab, back_slab], axis=1)
  return np.concatenate([front_slab, joined], axis=1)

#change to z
def S(cube):
  front_slab = cube[:,0:1,:]
  middle_slab = cube[:,1:2,:]
  middle_slab = Z(middle_slab)
  back_slab = cube[:,2:,:]
  joined = np.concatenate([middle_slab, back_slab], axis=1)
  return np.concatenate([front_slab, joined], axis=1)

#change to z
def F_prime(cube):
  front_slab = cube[:,0:1,:]
  middle_slab = cube[:,1:2,:]
  back_slab = cube[:,2:,:]
  back_slab = Z_prime(back_slab)
  joined = np.concatenate([middle_slab, back_slab], axis=1)
  return np.concatenate([front_slab, joined], axis=1)

#change to z
def F(cube):
  front_slab = cube[:,0:1,:]
  middle_slab = cube[:,1:2,:]
  back_slab = cube[:,2:,:]
  back_slab = Z(back_slab)
  joined = np.concatenate([middle_slab, back_slab], axis=1)
  return np.concatenate([front_slab, joined], axis=1)

#change to y
def U(cube):
  top_slab = cube[:1,:,:]
  top_slab = Y(top_slab)
  middle_slab = cube[1:2,:,:]
  bottom_slab = cube[2:,:,:]
  joined = np.concatenate([middle_slab, bottom_slab], axis=0)
  return np.concatenate([top_slab, joined], axis=0)

#change to y
def U_prime(cube):
  top_slab = cube[:1,:,:]
  top_slab = Y_prime(top_slab)
  middle_slab = cube[1:2,:,:]
  bottom_slab = cube[2:,:,:]
  joined = np.concatenate([middle_slab, bottom_slab], axis=0)
  return np.concatenate([top_slab, joined], axis=0)

#change to y
def E_prime(cube):
  top_slab = cube[:1,:,:]
  middle_slab = cube[1:2,:,:]
  middle_slab = Y(middle_slab)
  bottom_slab = cube[2:,:,:]
  joined = np.concatenate([middle_slab, bottom_slab], axis=0)
  return np.concatenate([top_slab, joined], axis=0)

#change to y
def E(cube):
  top_slab = cube[:1,:,:]
  middle_slab = cube[1:2,:,:]
  middle_slab = Y_prime(middle_slab)
  bottom_slab = cube[2:,:,:]
  joined = np.concatenate([middle_slab, bottom_slab], axis=0)
  return np.concatenate([top_slab, joined], axis=0)

#change to y
def D_prime(cube):
  top_slab = cube[:1,:,:]
  middle_slab = cube[1:2,:,:]
  bottom_slab = cube[2:,:,:]
  bottom_slab = Y(bottom_slab)
  joined = np.concatenate([middle_slab, bottom_slab], axis=0)
  return np.concatenate([top_slab, joined], axis=0)

#change to y
def D(cube):
  top_slab = cube[:1,:,:]
  middle_slab = cube[1:2,:,:]
  bottom_slab = cube[2:,:,:]
  bottom_slab = Y_prime(bottom_slab)
  joined = np.concatenate([middle_slab, bottom_slab], axis=0)
  return np.concatenate([top_slab, joined], axis=0)

core_moves = {
    "U": U,
    "U'": U_prime,
    "D":D,
    "D'":D_prime,
    "B":B,
    "B'": B_prime,
    "F": F,
    "F'": F_prime,
    "L":L,
    "L'":L_prime,
    "R": R,
    "R'": R_prime,
}

slices = {
    "M":M,
    "M'":M_prime,
    "S": S,
    "S'": S_prime,
    "E":E,
    "E'":E_prime,
}

orients = {
    "X":X,
    "X'":X_prime,
    "Y":Y,
    "Y'": Y_prime,
    "Z":Z,
    "Z'":Z_prime
}

moves = core_moves | slices | orients