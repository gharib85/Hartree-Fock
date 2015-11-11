from integrals import *

import numpy.linalg as la

def S_overlap(basis,N,R):
    """
    Compute overlap matrix.

    BASIS: Contraction coefficients of the STO-NG basis set.
    N: Number of electrons (dimensions of the matrix).
    R: Nuclear positions.
    """
    S = np.zeros((N,N))

    for i in range(N):
        for j in range(N):
            for c in basis[i]:
                for d in basis[j]:
                    S[i,j] += c[0].conjugate()*d[0] * overlap_ss(c[1],d[1],R[i],R[j])

    return S

def X_transform(S):
    """
    Compute the transformation matrix X using canonical orthogonalization.

    S: Overlap matrix.
    """

    s, U = la.eig(S)

    s = np.diag(s**(-1./2.))

    X = np.dot(U,s)

    return X

def T_kinetic(basis,N,R):
    """
    Compute kinetic operator matrix.

    BASIS: Contraction coefficients of the STO-NG basis set.
    N: Number of electrons (dimensions of the matrix).
    R: Nuclear positions.
    """
    T = np.zeros((N,N))

    for i in range(N):
        for j in range(N):
            for c in basis[i]:
                for d in basis[j]:
                    T[i,j] += c[0].conjugate()*d[0] * kinetic_ss(c[1],d[1],R[i],R[j])

    return T

def V_nuclear(basis,N,R,Zn,Rn):
    """
    Compute nuclear potential operator matrix.

    BASIS: Contraction coefficients of the STO-NG basis set.
    N: Number of electrons (dimensions of the matrix).
    Rn: Nuclear position
    Zn: Nuclear charge
    """
    Vn = np.zeros((N,N))

    for i in range(N):
        for j in range(N):
            for c in basis[i]:
                for d in basis[j]:
                    Vn[i,j] += c[0].conjugate()*d[0] * nuclear_ss(c[1],d[1],R[i],R[j],Zn,Rn)

    return Vn

def H_core(basis,N,R,Z):
    """
    Compute core Hamiltonian matrix.

    BASIS: Contraction coefficients of the STO-NG basis set.
    N: Number of electrons (dimensions of the matrix).
    R: Nuclear positions
    Z: Nuclear charges
    """

    H = T_kinetic(basis,N,R)

    for r,z in zip(R,Z):
        H += V_nuclear(basis,N,R,z,r)

    return H

def P_density(C,N):
    """
    Compute dansity matrix.

    C: coefficients matrix.
    N: Number of electrons (dimensions of the matrix).
    """

    P = np.zeros((N,N))

    for i in range(N):
        for j in range(N):
            for k in range(int(N/2)): #TODO Only for RHF
                P[i,j] += 2 * C[i,k] * C[j,k].conjugate()

    return P

def G_ee(basis,N,R,Z,P,ee):
    """
    Compute core Hamiltonian matrix.

    BASIS: Contraction coefficients of the STO-NG basis set.
    N: Number of electrons (dimensions of the matrix).
    R: Nuclear positions
    Z: Nuclear charges
    P: density matrix.
    EE: Two-electron integrals
    """

    G = np.zeros((N,N))

    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    G[i,j] += P[k,l] * (ee[i,j,k,l]  - 0.5 * ee[i,l,k,j])

    return G



if __name__ == "__main__":

    STO3G = [[(0.444635,0.168856),(0.535328,0.623913),(0.154329,3.42525)],
            [(0.444635,0.168856),(0.535328,0.623913),(0.154329,3.42525)]]

    N = 2

    Z = (1,1)

    R = (0.0,1.4)

    print("#####################")
    print("H2 : STO-3G BASIS SET")
    print("#####################")

    print("\nOverlap matrix S:")
    print(S_overlap(STO3G,N,R))

    print("\nKinetic operator T:")
    print(T_kinetic(STO3G,N,R))

    print("\nNuclear potential operator Vn (1st nucleus):")
    print(V_nuclear(STO3G,N,R,Z[0],R[0]))

    print("\nNuclear potential operator Vn (2nd nucleus):")
    print(V_nuclear(STO3G,N,R,Z[1],R[1]))

    print("\nCore Hamiltonian:")
    print(H_core(STO3G,N,R,Z))

    z1 = 2.0925 # He
    z2 = 1.24 # H

    STO3G = [[(0.444635,0.109818*z1**2),(0.535328,0.405771*z1**2),(0.154329,2.22766*z1**2)],
        [(0.444635,0.109818*z2**2),(0.535328,0.405771*z2**2),(0.154329,2.22766*z2**2)]]

    N = 2

    Z = (2,1)

    R = (0.0,1.4632)

    print("\n\n\n\n\n")
    print("#######################")
    print("HeH+ : STO-3G BASIS SET")
    print("#######################")

    print("\nOverlap matrix S:")
    print(S_overlap(STO3G,N,R))

    print("\nKinetic operator T:")
    print(T_kinetic(STO3G,N,R))

    print("\nNuclear potential operator Vn (1st nucleus):")
    print(V_nuclear(STO3G,N,R,Z[0],R[0]))

    print("\nNuclear potential operator Vn (2nd nucleus):")
    print(V_nuclear(STO3G,N,R,Z[1],R[1]))

    print("\nCore Hamiltonian:")
    print(H_core(STO3G,N,R,Z))
