# -*- coding: utf-8 -*-
"""
This file gives the dipole radiation (E and B field) in the far field, the full radiation (near field + far field) and the near field radiation only

@author: manu
"""
from pylab import *
import numpy
import time
import os
c=299792458.
pi=numpy.pi
mu0=4*pi*1e-7
eps0=1./(mu0*c**2)
multipleTimeSamples = False

def Hertz_dipole_ff (r, p, R, phi, f, t=0, epsr=1.):
	"""
	Calculate E and B field strength radaited by hertzian dipole(s) in the far field.
	p: array of dipole moments [[px0,py0,pz0],[px1,py1,pz1],...[pxn,pyn,pzn]]
	R: array of dipole positions [[X0,Y0,Z0],[X1,Y1,Z1],...[Xn,Yn,Zn]]
	r: observation point [x,y,z]
	f: array of frequencies [f0,f1,...]
	t: time
	phi: array with dipole phase angles (0..2pi) [phi0,phi1,...,phin]
	return: fields values at observation point r at time t for every frequency in f. E and B are (3 components,number of frequencies) arrays.
	"""
	nf = len(f)
	rprime = r-R  # r'=r-R
	if numpy.ndim(p) < 2:
		magrprime = numpy.sqrt(numpy.sum((rprime)**2))
		magrprimep = numpy.tile(magrprime, (len(f),1)).T
		phip = numpy.tile(phi, (len(f),1))
		w = 2*pi*f  # \omega
		k = w/c     # wave number
		krp = k*magrprimep  # k|r'|
		rprime_cross_p = numpy.cross(rprime, p) # r'x p
		rp_c_p_c_rp = numpy.cross(rprime_cross_p, rprime) # (r' x p) x r'
		expfac = numpy.exp(1j*(w*t-krp+phip.T))/(4*pi*eps0*epsr)
		phiOutput = numpy.exp(1j*(w*t-krp+phip.T))
		Ex = (w**2/(c**2*magrprimep**3) * expfac)* (numpy.tile(rp_c_p_c_rp[0],(nf,1))).T
		Ey = (w**2/(c**2*magrprimep**3) * expfac)* (numpy.tile(rp_c_p_c_rp[1],(nf,1))).T
		Ez = (w**2/(c**2*magrprimep**3) * expfac)* (numpy.tile(rp_c_p_c_rp[2],(nf,1))).T
		Bx = expfac/(magrprimep**2*c**3)*(w**2*numpy.tile(rprime_cross_p[0],(nf,1)).T)
		By = expfac/(magrprimep**2*c**3)*(w**2*numpy.tile(rprime_cross_p[1],(nf,1)).T)
		Bz = expfac/(magrprimep**2*c**3)*(w**2*numpy.tile(rprime_cross_p[2],(nf,1)).T)
		E = numpy.vstack((Ex,Ey,Ez))
		B = numpy.vstack((Bx,By,Bz))
	else:
		magrprime = numpy.sqrt(numpy.sum((rprime)**2,axis=1)) # |r'|
		magrprimep = numpy.tile(magrprime, (len(f),1)).T
		phip = numpy.tile(phi, (len(f),1))
		fp = numpy.tile(f,(len(magrprime),1))
		w = 2*pi*fp  # \omega
		k = w/c     # wave number
		krp = k*magrprimep  # k|r'|
		rprime_cross_p = numpy.cross(rprime, p) # r'x p
		rp_c_p_c_rp = numpy.cross(rprime_cross_p, rprime) # (r' x p) x r'
		expfac = numpy.exp(1j*(w*t-krp+phip.T))/(4*pi*eps0*epsr)
		phiOutput = numpy.exp(1j*(w*t-krp+phip.T))
		Ex = (w**2/(c**2*magrprimep**3) * expfac)* (numpy.tile(rp_c_p_c_rp[:,0],(nf,1))).T
		Ey = (w**2/(c**2*magrprimep**3) * expfac)* (numpy.tile(rp_c_p_c_rp[:,1],(nf,1))).T
		Ez = (w**2/(c**2*magrprimep**3) * expfac)* (numpy.tile(rp_c_p_c_rp[:,2],(nf,1))).T
		Bx = expfac/(magrprimep**2*c**3)*(w**2*numpy.tile(rprime_cross_p[:,0],(nf,1)).T)
		By = expfac/(magrprimep**2*c**3)*(w**2*numpy.tile(rprime_cross_p[:,1],(nf,1)).T)
		Bz = expfac/(magrprimep**2*c**3)*(w**2*numpy.tile(rprime_cross_p[:,2],(nf,1)).T)
		E = numpy.vstack((numpy.sum(Ex,axis=0),numpy.sum(Ey,axis=0),numpy.sum(Ez,axis=0)))
		B = numpy.vstack((numpy.sum(Bx,axis=0),numpy.sum(By,axis=0),numpy.sum(Bz,axis=0)))
	return E,B,phiOutput


def createDirectory():
	folderName = time.strftime("%Y%m%d-%H%M%S")
	directory = os.getcwd()
	path = (directory + '\\' + folderName)
	if not os.path.exists(path):
		os.makedirs(path)
	return path

if __name__ == "__main__":
	#observation points
	nx = 401 # number of points
	xmax = 2 #meters
	nz = 201 # number of points
	zmax = 1 #meters
	y = 2 # above dipole
	x=numpy.linspace(-xmax,xmax,nx)
	z=numpy.linspace(-zmax,zmax,nz)
	observationTime =  1 #obs. time (nanoseconds) used if multipleTimeSamples = False

	#dipole
	freq=numpy.array([1000e6])
	#dipole moment
	#total time averaged radiated power P= 1 W dipole moment => |p|=sqrt(12pi*c*P/muO/w**4)
	Pow=1
	norm_p=sqrt(12*pi*c*Pow/(mu0*(2*pi*freq)**4))
	#dipole moment
	p=numpy.array([0,0,norm_p])
	R=numpy.array([0,0,0])
	#dipole phases
	phases_dip=1
	path = createDirectory()
	print("Computing the radiation...")
	
	
	if multipleTimeSamples == True:
		nt=100
		t0=1/freq/10
		t1=5/freq
		nt=int(t1/t0)
		#nt = 1
		t=numpy.linspace(t0,t1,nt)
		fig = figure(num=1,figsize=(10,6),dpi=300)
		for k in range(nt): #t[k] is the time sample
			startTime = time.time()
			P=numpy.zeros((nx,nz))
			for i in range(nx):
				for j in range(nz):
					r=array([x[i],y,z[j]])
					E,B,phip = Hertz_dipole_ff(r, p, R, phases_dip, freq, t[k], epsr=1.)
					S=real(E)**2#0.5*numpy.cross(E.T,conjugate(B.T))
					P[i,j]=sum(S)
			print('%2.1f/100'%((k+1)/nt*100))
			calcTime=time.time()-startTime
			#Radiation diagram
			pcolor(x,z,np.log10(P[:,:].T),vmin=np.amin(P), vmax=np.amax(P), cmap='hot')
			#pcolor(x,z,P[:,:].T, cmap='hot')
			colorbar()
			fname = 'img_%s' %(k)
			#clim(0,1000)
			axis('scaled')
			xlim(-xmax,xmax)
			ylim(-zmax,zmax)
			xlabel(r'$x/$m')
			ylabel(r'$z/$m')
			title(r'$t=%2.2f$ ns'%(t[k]/1e-9))
			print('Saving frame' + fname)
			print('Calculation Time: ' + time.strftime("%H:%M:%S", time.gmtime(calcTime)))
			fig.savefig(path + '\\' + fname +'.png',bbox = 'tight')
			clf()
			magData = P[:,:].T #save magnitude of electric field
			phaseData = phip[:,:] #save phase
			numpy.savetxt(path + "\\magData" + fname + ".csv",magData,delimiter = ',', fmt = "%s")
			numpy.savetxt(path + "\\phaseData" + fname + ".csv",phaseData,delimiter = ',', fmt = "%s")
	else: #single time sample
		startTime = time.time()
		fig = figure(num=1,figsize=(10,6),dpi=300)
		#for k in range(nt): #t[k] is the time sample
		P=numpy.zeros((nx,nz))
		phipArr = numpy.zeros((nx,nz))
		for i in range(nx):
			for j in range(nz):
				r=array([x[i],y,z[j]])
				E,B,phip = Hertz_dipole_ff(r, p, R, phases_dip, freq, observationTime, epsr=1.)
				S=real(E)**2#0.5*numpy.cross(E.T,conjugate(B.T))
				P[i,j]=sum(S)
				phipArr[i,j] = real(phip) #save phase info into array
		calcTime=time.time()-startTime
		#Radiation diagram
		pcolor(x,z,P[:,:].T, cmap='hot')
		colorbar()
		fname = 'EfieldPlot' + str(observationTime) + 'ns'
		#clim(0,1000)
		axis('scaled')
		xlim(-xmax,xmax)
		ylim(-zmax,zmax)
		xlabel(r'$x/$m')
		ylabel(r'$z/$m')
		title('Electric Field Plot at ' + str(observationTime) + 'ns')
		print('Saving frame' + fname)
		print('Calculation Time: ' + time.strftime("%H:%M:%S", time.gmtime(calcTime)))
		fig.savefig(path + '\\' + fname +'.png',bbox = 'tight')
		clf()
		numpy.savetxt(path + "\\magData.csv",P[:,:].T,delimiter = ',', fmt = "%s") #save magnitude of electric field
		numpy.savetxt(path + "\\phaseData.csv",phipArr[:,:],delimiter = ',', fmt = "%s") #save phase