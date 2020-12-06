
import math 
def round_up_to_even(f):
    return math.ceil(f / 2.) * 2

def round_down_to_even(f):
    return math.floor(f / 2.) * 2

def plot_best(chi2,grid,data,plot_fig,fontsize=16,ticksize=14,output=None,yticks=[],yticklabels=[]):
    [tau_grid,tdelay_grid,extinction_grid,m2_grid]=grid

    itau_best,it_best,iav_best,im_best=np.where(chi2==np.nanmin(chi2))
    itau_best=itau_best[0]
    it_best=it_best[0]
    iav_best=iav_best[0]
    im_best=im_best[0]
    tau_best=tau_grid[itau_best]
    ti_best=tdelay_grid[it_best]
    av_best=extinction_grid[iav_best]
    m2_best=m2_grid[im_best]
    print "min chi-square: %.2e, tbest=%.1f Gyr, taubest=%.1f Myr, Avbest=%.1f,logm=%.2f"%(np.nanmin(chi2),ti_best,tau_best,av_best,np.log10(m2_best))
    
    age = np.where(abs(data[itau_best].output_age*1e-3-float(ti_best))==abs(data[itau_best].output_age*1e-3-float(ti_best)).min())
    i_age = age[0][0]
    
    lambda_rest=data[itau_best].lambda_cont
    L_rest=data[itau_best].lum_cont[i_age,:]

    extinction_av=av_best
    ext_rest=0*np.ones_like(lambda_rest)
    lambda_range=np.where((lambda_rest>=limits_rest[0]/(1+z[igal]))&(lambda_rest<=limits_rest[1]/(1+z[igal])))                
    ext_rest[lambda_range]=extinction(lambda_rest[lambda_range],a_v=extinction_av,r_v=extinction_rv,model=extinction_model)
    L_rest_ext=L_rest*10**(-0.4*ext_rest)+m2_best*data_burst2.lum_cont[i_burst2,:]

    lambda_obs=lambda_rest*(1+z[igal])
    F_obs=L_rest_ext/(4.*np.pi*(DL_pc[igal]*parsec*100)**2)/(1+z[igal]) # erg/s/cm2/A/Mstar

    # F105W
    filtF105W  = np.interp(lambda_obs,lambda_F105W,filt_F105W)
    filtF105W[np.where(filtF105W<1e-2)]=0
    Mformed=1.#(1.-exp(-delay/1.))
    FmeanF105W=simps(F_obs*filtF105W,lambda_obs)/simps(filtF105W,lambda_obs)/Mformed #  10^-16 erg/s/cm2/A/Mstar
    Mstar_result_F105W=F105W[igal]/FmeanF105W*1e-16*1e-13 # 10^13 Msun
    dMstar_result_F105W=Mstar_result_F105W*max(dF105W[igal],dFmin*F105W[igal])/F105W[igal]

    # F140W
    filtF140W  = np.interp(lambda_obs,lambda_F140W,filt_F140W)
    filtF140W[np.where(filtF140W<1e-2)]=0
    Mformed=1.#(1.-exp(-delay/1.))
    FmeanF140W=simps(F_obs*filtF140W,lambda_obs)/simps(filtF140W,lambda_obs)/Mformed #  10^-16 erg/s/cm2/A/Mstar
    Mstar_result_F140W=F140W[igal]/FmeanF140W*1e-16*1e-13 # 10^13 Msun
    dMstar_result_F140W=Mstar_result_F140W*max(dF140W[igal],dFmin*F140W[igal])/F140W[igal]
    
    # F160W
    filtF160W  = np.interp(lambda_obs,lambda_F160W,filt_F160W)
    filtF160W[np.where(filtF160W<1e-2)]=0
    Mformed=1.#(1.-exp(-delay/1.))
    FmeanF160W=simps(F_obs*filtF160W,lambda_obs)/simps(filtF160W,lambda_obs)/Mformed #  10^-16 erg/s/cm2/A/Mstar
    Mstar_result_F160W=F160W[igal]/FmeanF160W*1e-16*1e-13 # 10^13 Msun
    dMstar_result_F160W=Mstar_result_F160W*max(dF160W[igal],dFmin*F160W[igal])/F160W[igal]
    
    Mstar_array=np.array([Mstar_result_F105W,Mstar_result_F140W,Mstar_result_F160W])
    dMstar_array=np.array([dMstar_result_F105W,dMstar_result_F140W,dMstar_result_F160W])
    
    weights=1./dMstar_array**2
    nonan_indices = np.where(np.logical_not(np.isnan(Mstar_array)))[0]
    Mstar_result=np.average(Mstar_array[nonan_indices], weights=weights[nonan_indices])
    dMstar_result=np.sqrt(sum((dMstar_array/Mstar_array)**2))

    F105W_result=Mstar_result*FmeanF105W*1e29 # 10^-16 erg/s/cm2/A/Mstar
    F140W_result=Mstar_result*FmeanF140W*1e29 # 10^-16 erg/s/cm2/A/Mstar
    F160W_result=Mstar_result*FmeanF160W*1e29 # 10^-16 erg/s/cm2/A/Mstar                

    dF105W_result=dMstar_result*FmeanF105W*1e29 # 10^-16 erg/s/cm2/A/Mstar
    dF140W_result=dMstar_result*FmeanF140W*1e29 # 10^-16 erg/s/cm2/A/Mstar
    dF160W_result=dMstar_result*FmeanF160W*1e29 # 10^-16 erg/s/cm2/A/Mstar     
    
    tau_best_all[igal]=tau_best
    t_best_all[igal]=ti_best
    av_best_all[igal]=av_best
    m2_best_all[igal]=m2_best
    Mstar_best_all[igal]=Mstar_result
    dMstar_best_all[igal]=dMstar_result
    F105W_best_all[igal]=F105W_result
    F140W_best_all[igal]=F140W_result
    F160W_best_all[igal]=F160W_result
    dF105W_best_all[igal]=dF105W_result
    dF140W_best_all[igal]=dF140W_result
    dF160W_best_all[igal]=dF160W_result
    chi2_all.append(chi2)
    Mstar_all.append(Mstar_matrix)
    chi2_best_all[igal]=np.nanmin(chi2)
          
    if plot_fig:
        plt.figure(figsize=(10,8))
        plt.clf()
        ax1=plt.gca()
        plt.xlim(limits_rest[0],limits_rest[1]) 
        ax1.text(0.01,1.015,r'$\rm %s$'%name[igal],transform=ax1.transAxes,fontsize=fontsize)
        ax1.text(1,1.015,r'$t_{\rm delay}=%.1f$ $\rm Gyr,$ $\tau=%.1f$ $\rm Gyr,$ $A_v=%.1f,$ $\log(m)=%.1f$'%(float(ti_best),float(tau_best/1e3),float(av_best),np.log10(m2_best)),horizontalalignment="right",transform=ax1.transAxes,fontsize=fontsize)
        ax1.text(0.02,0.02,r'$\log(\chi^2)=%.1f,$ $M_0=%.1f \times 10^{13} M_\odot$'%(np.log10(np.nanmin(chi2)),float(Mstar_result)),transform=ax1.transAxes,fontsize=fontsize)
        
        lambda_range=np.where((lambda_obs>=limits_rest[0])&(lambda_obs<=limits_rest[1]))
        ax1.plot(lambda_obs[lambda_range],(Mstar_result*F_obs)[lambda_range]*10**(13+16),color='k',zorder=2)            
        
        ax1.errorbar(lcen_F105W,(Mstar_result*FmeanF105W)*10**(13+16),color=colors_Z[0],markeredgecolor=colors_Z[0],zorder=1,marker='o',markersize=10,capsize=1,alpha=0.7)
        ax1.errorbar(lcen_F140W,(Mstar_result*FmeanF140W)*10**(13+16),color=colors_Z[1],markeredgecolor=colors_Z[1],zorder=1,marker='o',markersize=10,capsize=1,alpha=0.7)
        ax1.errorbar(lcen_F160W,(Mstar_result*FmeanF160W)*10**(13+16),color=colors_Z[2],markeredgecolor=colors_Z[2],zorder=1,marker='o',markersize=10,capsize=1,alpha=0.7)
        
        ax1.errorbar(lcen_F105W,F105W[igal],yerr=max(dF105W[igal],dFmin*F105W[igal]),xerr=FWHM_F105W/2.,color=colors_Z[0],zorder=3,capsize=5,capthick=2,label=r'$\rm F105W$',lw=2)
        ax1.errorbar(lcen_F140W,F140W[igal],yerr=max(dF140W[igal],dFmin*F140W[igal]),xerr=FWHM_F140W/2.,color=colors_Z[1],zorder=3,capsize=5,capthick=2,label=r'$\rm F140W$',lw=2)
        ax1.errorbar(lcen_F160W,F160W[igal],yerr=max(dF160W[igal],dFmin*F160W[igal]),xerr=FWHM_F160W/2.,color=colors_Z[2],zorder=3,capsize=5,capthick=2,label=r'$\rm F160W$',lw=2)
        
        ax1.set_xticks([8000,10000,12000,14000,16000,18000,20000])
        ax1.set_xticklabels([r'$8000$',r'$10000$',r'$12000$',r'$14000$',r'$16000$',r'$18000$',r'$20000$'],fontsize=ticksize)
        ax1.set_yticks(yticks)
        ax1.set_yticklabels(yticklabels,fontsize=ticksize)
        
        line1 = Line2D([0,1],[0,1],linestyle='-', color=colors_Z[0])
        line2 = Line2D([0,1],[0,1],linestyle='-', color=colors_Z[1])
        line3 = Line2D([0,1],[0,1],linestyle='-', color=colors_Z[2])
        
        ax1.set_xlim(limits_rest[0],20000)
        ax1.set_xlabel(r'$\lambda_{\rm obs}$ $\rm [\AA]$',fontsize=fontsize)
        ax1.set_ylabel(r'$F_{\rm \lambda, obs}$ $\rm [10^{-16} erg/s/cm^2/\AA]$',fontsize=fontsize)
        legend=plt.legend([line1,line2,line3],['F105W','F140W','F160W'],loc='lower right',frameon=True,fontsize=fontsize) 
        frame = legend.get_frame()
        frame.set_color('w')
        frame.set_edgecolor('w')
        
        ax1.tick_params(axis='both', which='major', labelsize=ticksize)
        
        plt.savefig(output)
        