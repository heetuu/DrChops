pro quick_rebin06_10m,str,ebcn,cntsnew,errcntsnew,TBKG=tbkg,		$
			ei=ei,emin=emin,emax=emax,nepts=nepts,  $
			mask=mask,eff=eff,hmin=hmin,hmax=hmax

;procedure to rebin data into constant-E bins by pro-rating counts based
;on the overlap of old and new bins.
;Parameters:
;	str: Pharos data structure. Created and initialized beforehand.
;	cntsnew:	array of counts per new bin.
;	errcntsnew: errors assocoated with new counts
;	ebcn:	array of new energy bin centers. Will be init'd here
;   tbkg: estimated time-independent background per pixel
;	ei:	scalar incident energy
;
;The code is designed to have a two dimensional array passed to it,
;where the first dimension is energy, and the second dimension is angle.
;Angle and energy are decoupled for this operation, so this is just a
;convenient way to work on several (200-900) angles at once.
;
;first,  get array sizes,  do tedious checking of sizes.
;TK 07/01, from a long line of Rob Robinson/TK routines
;
;modified 08/02 to accept a three-dimensional array for counts old and
;a two dimensional array for counts_new. Need to run once for each height
;in the detector tube, as each height will have it own energy array.
;
;Does NOT multiply by DeltaT/DeltaE
;
;Does take care of k'/k.
;
;RJM 8/31/02 Modified to use with Pharos data reduction software. Designed to
; pass a data structure, rather than all of the individual arrays. Now takes
; time-of-flight array, as opposed to old energy array
;
;RJM 11/12/02 now performs detector efficiency correction when EFF flag 
;is set in call to quick_rebin
;
;RJM 1/15/03 allows range of detector heights to be summed using hmin and hmax
;
; Ask for info about energy rebin and calculate bin boundaries and centers
;
IF (N_ELEMENTS(tbkg) EQ 0) THEN tbkg=0.
IF (N_ELEMENTS(ei) EQ 0) THEN READ,ei,PROMPT='Enter incident energy (meV): '
IF ((N_ELEMENTS(emin) OR N_ELEMENTS(emax)) EQ 0) THEN READ,emin,emax,			$
   PROMPT='Enter minimum and maximum energy transfer bin centers (meV): '
IF (N_ELEMENTS(nepts) EQ 0) THEN READ,nepts,PROMPT='Enter number of energy transfer bin centers: '
ebcn=emin+(emax-emin)*FINDGEN(nepts)/FLOAT(nepts-1)
ebn=emin+(emax-emin)*(FINDGEN(nepts+1)-0.5)/FLOAT(nepts-1)
;
IF emax GE ei THEN BEGIN
	print,'You fool! Max energy transfer cannot be greater than incident energy'
	RETURN
ENDIF
;
tstart=systime(1)	;gotta know!
; RJM 8/31/02 ebo is now calculated from the time boundaries and the
; entered energy bin boundaries
;
sz=SIZE(str.big,/DIMENSIONS)
; Various spectrometer distances
;
	l1=18.
	l2=2.1
	l3=FLTARR(376)
;
; Read in detactor angles in order to calculate distances to low angle tubes
;
	detectorangle_10m,detang
;
; Low-angle bank
;
	FOR i=0,39 DO l3[i]=10.0/cos(!pi*detang[i]/180.)
;
; Wide-angle bank (fudge factor supposedly due to non-centricity of sample)
;
	FOR i=40,375 DO l3[i]=4.013
;      -float(375-i)*.016/335
;
; Convert tof to e, note that ebo depends on [time,height,det#]
; since each pixel in general has a unique secondary flight path length array
; lp[height,det#].
; For quick rebin, only consider distance to center of tube
;
ndet=sz[2]
lp=FLTARR(ndet)
;
	FOR j=0,375 DO BEGIN
		lp[j]=SQRT(l3[j]*l3[j])
	ENDFOR
;
; Find min and max time-of-flight bin boundaries for each pixel given
; emin and emax. Store as time array indices
;
vi=SQRT(ei/5.227e6)	   ;in m/us
vfmax=SQRT((ei-emin)/5.227e6)
vfmin=SQRT((ei-emax)/5.227e6)
tof=str.big_time		;TOF bin boundaries
dt=tof[1]-tof[0]
tof_min=MIN(tof)
imin=INTARR(ndet)
imax=INTARR(ndet)
;
	FOR j=0,375 DO BEGIN
		tmin=(l1+l2)/vi+lp[j]/vfmax
		tmax=(l1+l2)/vi+lp[j]/vfmin
		imin[j]=FIX((tmin-dt/2.-tof_min)/dt)
		imax[j]=FIX((tmax-dt/2.-tof_min)/dt)
	ENDFOR
;
;declare new arrays
cntsnew=fltarr(nepts,ndet)
errcntsnew=fltarr(nepts,ndet)
;
; Remove bad detectors
;
bigmask=FLTARR(376)
bigmask[*]=1.
IF (N_ELEMENTS(mask) NE 0) THEN bigmask[mask]=0.
;
;loop over detectors
	FOR k=0,375 DO BEGIN
;Calculate ebo for detector k
neold=imax[k]-imin[k]		;number of old energy bin centers
ebo=FLTARR(neold+1)				;define old bin boundaries and calculate
cntsold=FLTARR(neold)
errcntsold=FLTARR(neold)
imin_sc=imin[k]
imax_sc=imax[k]
FOR m=imin_sc,imax_sc-1 DO BEGIN
	ebo[m-imin_sc]=ei*(1.-(lp[k]/(vi*tof[m]-l1-l2))^2)
	cntsold[m-imin_sc]=TOTAL(str.big[m,hmin:hmax,k]-tbkg,2)*bigmask[k]
	errcntsold[m-imin_sc]=SQRT(TOTAL(str.big[m,hmin:hmax,k],2))*bigmask[k]
ENDFOR
ebo[neold-1]=ei*(1.-(lp[k]/(vi*tof[imax_sc]-l1-l2))^2)
;Next,  two loops,  one over the old energy bins,  the other over the new.
;i indexes the new, j the old.
		i=0
		j=0
		While i LT nepts-1 DO BEGIN
			While j LT neold-1  DO BEGIN

;First,  increment j until the right edge of the old energy bin is beyond the left
;edge of the current new energy bin:
;                ebo[j]            ebo[j+1]
;Old Bin:          |____________________|
;New bin:              |_______|
;                 ebn[i]       ebn[i+1]

				WHILE (ebo[j+1] LT ebn[i]) AND (j LT neold-1) DO j=j+1

;This should be done once, just to skip past old bin points that might not
;be interesting
;Once this is done,  put the old bin into the new bin
;For PHAROS data, Array[time,height,det#]

				overlap=lesser(ebo[j+1],ebn[i+1])-greater(ebo[j],ebn[i])
				cntsnew[i,k]=cntsnew[i,k]+cntsold[j]*dt*overlap/(ebo[j+1]-ebo[j])

				;add errors in quadrature
				errcntsnew[i,k]= errcntsnew[i,k]+(errcntsold[j]*dt*overlap/(ebo[j+1]-ebo[j]))^2

;If the right edge of the old bin lies beyond the right edge of the new bin,  increment the new bin
;otherwise move on to the next old bin.

				IF (ebo[j+1] GT ebn[i+1]) AND (i LT nepts-1) THEN i=i+1 ELSE j=j+1
			ENDWHILE	;While j LT numenrgold-1  DO BEGIN

			i=i+1
		ENDWHILE	;While i LT numenrgnew-1 DO BEGIN
	ENDFOR			;ends FOR k=0,numdets
errcntsnew=Sqrt(errcntsnew)


;Multiply by k_i/k_f = Sqrt[E_i/E_f] = Sqrt[E_i/(E_i-Delta_E)]
;cntsnew=fltarr(numenrgnew,numdets,numheights)
;errcntsnew=fltarr(numenrgnew,numdets,numheights)

FOR i=0,nepts-1 do errcntsnew[i,*]=errcntsnew[i,*]*Sqrt(ei/(ei-ebcn[i]))
FOR i=0,nepts-1 do cntsnew[i,*]=cntsnew[i,*]*Sqrt(ei/(ei-ebcn[i]))

;
; Correct for detector efficiency dependence on final neutron energy
; Note that detectors 0:263 are 10 atm, 264:375 are 6 atm.
;
	IF (N_ELEMENTS(eff) NE 0) THEN BEGIN
	   ef=FLTARR(nepts)
	   ef[*]=ei-ebcn[*]
	   EF_EFFICIENCY,ef,eff6,eff10
	   plot,ebcn,eff10,xtitle='Energy Transfer (meV)',ytitle='Efficiency'
	   oplot,ebcn,eff6
	   FOR i=0,nepts-1 DO BEGIN
	      cntsnew[i,264:375]=cntsnew[i,264:375]/eff6[i]
	      errcntsnew[i,264:375]=errcntsnew[i,264:375]/eff6[i]
	      cntsnew[i,0:263]=cntsnew[i,0:263]/eff10[i]
	      errcntsnew[i,0:263]=errcntsnew[i,0:263]/eff10[i]
	   ENDFOR
	ENDIF
;
tfinish=systime(1)
print,'elapsed time =',tfinish-tstart

return
end

;Two functions to get the lesser or greater of the arguments
;Recall IDL syntax "a ? b : c" returns b if a is true,  c if a is false.
function lesser,a,b
c=a LT b ? a:b
return,c
end

function greater,a,b
c= a GT b ? a:b
return,c
end
