from matplotlib.colors import LogNorm

def plot_grid(chi2,grid,best_vals,var_names,var_labels,limits,Nlvls=100,output=None,fig_title=None,num=None,fontsize=16,ticksize=14,ticks=[],ticklabels=[],chi2_ticks=[],chi2_ticklabels=[]):
    npars=np.size(var_names)
    
    fig, axes = plt.subplots(npars, npars,figsize=(10,8))
    for i, par1 in enumerate(var_names):
        for j, par2 in enumerate(var_names):
                # parameter vs chi2 in case of only one parameter
                #if npars == 1:
                #    axes.plot(, result.brute_Jout, 'o', ms=3)
                #    axes.set_ylabel(r'$\chi^{2}$')
                #    axes.set_xlabel(varlabels[i])
                #    if best_vals:
                #        axes.axvline(best_vals[par1].value, ls='dashed', color='r')
    
                # parameter vs chi2 profile on top
                if i == j and j < npars:
                    #if i == 0:
                    #    axes[0, 0].axis('off')
                    ax = axes[i, j]
                    ax.tick_params(axis='both', which='both', labelsize=ticksize,width=1,length=5,zorder=10)
                    red_axis = tuple([a for a in range(npars) if a != i])
                    chi2_axis=np.log10(np.nanmin(chi2,axis=red_axis))
                    #ax.plot(grid[i],chi2_axis,'o',c='k',ms=3,zorder=1)
                    ax.plot(grid[i],chi2_axis,'k',lw=2,zorder=1)
                    ylim_ax=ax.get_ylim()
                    #ax.axhline(np.log10((np.nanmin(chi2)+1)), ls=':', color='k',lw=1.5,zorder=0)
                    ax.set_ylabel(r'$\log(\chi^{2})$',fontsize=fontsize)
                    ax.set_xlim(limits[i])
                    ax.set_ylim(ylim_ax)
                    ax.yaxis.set_label_position("right")
                    ax.yaxis.set_ticks_position("right")
                    ax.set_yticks(chi2_ticks[i])
                    ax.set_yticklabels(chi2_ticklabels[i])
                        
                    ax.tick_params(axis='both', which='major', labelsize=ticksize)
                    if j!=npars-1:
                        ax.set_xticks([])
                    else:
                        ax.set_xticks(ticks[i])
                        ax.set_xticklabels(ticklabels[i])
                        
                    if best_vals:
                        ax.axvline(best_vals[i], ls='-', color='r',lw=1.5,zorder=1)
                    
                    if j==npars-1:
                        ax.set_xlabel(var_labels[i],fontsize=fontsize)
                
                # parameter vs chi2 profile on the left
                #elif j == npars-1 and i==npars-1:
                #    ax = axes[i, j]
                #    red_axis = tuple([a for a in range(npars) if a != i])
                #    ax.plot(np.log10(np.nanmin(chi2,axis=red_axis)),
                #            grid[i], 'o', ms=3)
                #    ax.invert_xaxis()
                #    ax.set_ylabel(var_labels[i])
                #    ax.set_ylim(limits[i])
                #   ax.yaxis.set_label_position("right")
                #   ax.yaxis.set_ticks_position('right')
                #    #ax.set_xlim(log10(chi2_limits))
                #
                #    if i != npars-1:
                #        ax.set_xticks([])
                #    elif i == npars-1:
                #        ax.set_xlabel(r'$\log\chi^{2}$')
                #    if best_vals:
                #        ax.axhline(best_vals[i], ls='dashed', color='r',lw=2)
                        
                # contour plots for all combinations of two parameters
                elif j > i:
                    ax = axes[j, i]
                    ax.tick_params(axis='both', which='both', labelsize=ticksize,width=1,length=5,zorder=10)
                    red_axis = tuple([a for a in range(npars) if a not in (i, j)])
                    X, Y = np.meshgrid(grid[i],
                                    grid[j])
                    #lvls1 = np.linspace(np.nanmin(chi2),
                    #                    np.nanmedian(chi2)/2.0, 7, dtype='int')
                    #lvls2 = np.linspace(np.nanmedian(chi2)/2.0,
                    #                    np.nanmedian(chi2), 3, dtype='int')
                    #lvls = np.unique(np.concatenate((lvls1, lvls2)))
                    #lvls=np.linspace(chi2_limits[0],chi2_limits[1],51)
                    cmin=np.nanmin(np.nanmin(chi2,axis=red_axis).flatten())
                    cmax=np.nanmax(np.nanmin(chi2,axis=red_axis).flatten())
                    #if cmax/cmin>1e3:
                    lvls=np.logspace(np.log10(cmin),np.log10(cmax),Nlvls)
                    #else:
                    #    lvls=np.linspace(cmin,cmax,Nlvls)
                    ax.contourf(X.T, Y.T, np.nanmin(chi2,axis=red_axis),
                                lvls, norm=LogNorm(),cmap='jet',zorder=3)
                    #ax.contour(X.T, Y.T, np.nanmin(chi2,axis=red_axis),
                    #            [np.nanmin(chi2)+1],colors='w',lw=0.8,zorder=3)
                    ax.contour(X.T, Y.T, np.nanmin(chi2,axis=red_axis),
                                [np.nanmin(chi2)+1],colors='w',linestyles='-',linewidths=2,zorder=4)
                    ax.contour(X.T, Y.T, np.nanmin(chi2,axis=red_axis),
                                [np.nanmin(chi2)+1],colors='k',linestyles='--',dashes=(2,2),linewidths=2,zorder=5)
                    #ax.set_yticks([])
                    ax.set_xlim(limits[i])
                    ax.set_ylim(limits[j])
                    
                    if best_vals:
                        ax.axvline(best_vals[i], ls='-', color='r',lw=2,zorder=6)
                        ax.axhline(best_vals[j], ls='-', color='r',lw=2,zorder=6)
                        #ax.plot(best_vals[i], best_vals[j], 'rs', ms=3,zorder=7)
                    
                    if j != npars-1:
                        ax.set_xticks([])
                    elif j == npars-1:
                        ax.set_xlabel(var_labels[i],fontsize=fontsize)
                        ax.set_xticks(ticks[i])
                        ax.set_xticklabels(ticklabels[i])

                    if i == 0:
                        ax.set_ylabel(var_labels[j],fontsize=fontsize)
                        ax.set_yticks(ticks[j])
                        ax.set_yticklabels(ticklabels[j])

                    else:
                        ax.set_yticks([])
                    
                    if j - i >= 1:
                        axes[i, j].axis('off')
                                                      
    if fig_title is not None:
        fig.suptitle(fig_title)
            
    if output is not None:
        plt.savefig(output)
        
        