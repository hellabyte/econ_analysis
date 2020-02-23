from hellaPy import *
from numpy import *
from pylab import *
from matplotlib.ticker import MultipleLocator,LinearLocator
import pandas
f1 = 'dat/DGS1.csv'
f2 = 'dat/DGS2.csv'
f3 = 'dat/DGS3.csv'
f5 = 'dat/DGS5.csv'
f10= 'dat/DGS10.csv'
fJ = 'dat/BAMLH0A3HYCEY.csv'

def get_df(f):
  df = pandas.read_csv(f)
  key= f.split('/')[-1].split('.')[0]
  df.DATE = df.DATE.astype('datetime64[ns]')
  df[key][df[key] == '.'] = nan
  df[key] = df[key].astype(float)
  return df.set_index('DATE')

df1 = get_df(f1)
df2 = get_df(f2).reindex(df1.index)
df3 = get_df(f3).reindex(df1.index)
df5 = get_df(f5).reindex(df1.index)
df10= get_df(f10).reindex(df1.index)
dfJ = get_df(fJ).reindex(df1.index)

dfd= {
  'DATE'    : df1.index,
  'DGS1'    : df1.DGS1,
  'DGS2'    : df2.DGS2,
  'DGS3'    : df3.DGS3,
  'DGS5'    : df5.DGS5,
  'DGS10'   : df10.DGS10,
  'JUNK'    : dfJ.BAMLH0A3HYCEY,
  'y1ratio' : df1.DGS1 / df10.DGS10,
  'y2ratio' : df2.DGS2 / df10.DGS10,
  'y5ratio' : df5.DGS5 / df10.DGS10,
  'x1ratio' : df1.DGS1 / df5.DGS5,
  'x2ratio' : df2.DGS2 / df5.DGS5,
  'x3ratio' : df3.DGS3 / df5.DGS5,
  'jratio'  : df10.DGS10 / dfJ.BAMLH0A3HYCEY,
}

df = pandas.DataFrame(dfd)

recessions = [
  [ datetime64('1969-01-01'), datetime64('1969-04-01'), datetime64('1969-10-01'), datetime64('1970-01-01') ],
  [ datetime64('1973-07-01'), datetime64('1973-10-01'), datetime64('1975-01-01'), datetime64('1975-04-01') ],
  [ datetime64('1979-01-01'), datetime64('1979-04-01'), datetime64('1980-04-01'), datetime64('1980-07-01') ],
  [ datetime64('1981-01-01'), datetime64('1981-04-01'), datetime64('1982-04-01'), datetime64('1982-07-01') ],
  [ datetime64('1989-07-01'), datetime64('1989-10-01'), datetime64('1991-01-01'), datetime64('1991-04-01') ],
  [ datetime64('2000-10-01'), datetime64('2001-01-01'), datetime64('2001-07-01'), datetime64('2001-10-01') ],
  [ datetime64('2007-07-01'), datetime64('2007-10-01'), datetime64('2009-04-01'), datetime64('2009-07-01') ],
]

ext= [-1,2]
figure(1,figsize=(12,4)); clf()
ax = gca()
plot([datetime64('1955'),datetime64('2025')],ones(2),'r-',lw=2,alpha=.5)
for recession in recessions:
  plot([recession[ 0]]*2,ext,'--k',alpha=.3)
  plot([recession[-1]]*2,ext,'--k',alpha=.3)
  fill_betweenx(ext,*recession[:2],color='k',alpha=.1)
  fill_betweenx(ext,*recession[1:-1],color='k',alpha=.2)
  fill_betweenx(ext,*recession[-2:],color='k',alpha=.1)
#plot(df.DATE,df.jratio,'b-')
plot(df.DATE,df.y1ratio,'-',c='#000000',label='$(1,10)$',zorder=110)#alpha=1.0)
#plot(df.DATE,df.y2ratio,'-',c='#333333',label='$(2,10)$',zorder=109)#alpha=0.7)
plot(df.DATE,df.y5ratio,'-',c='#777777',label='$(5,10)$',zorder=108)#alpha=0.4)
plot(df.DATE,df.x1ratio,'-',c='#0000ff',label='$(1, 5)$',zorder=107)#alpha=1.0)
#plot(df.DATE,df.x2ratio,'-',c='#0000cc',label='$(2, 5)$',zorder=106)#alpha=0.7)
plot(df.DATE,df.x3ratio,'-',c='#000099',label='$(3, 5)$',zorder=105)#alpha=0.4)
l = legend(loc='lower left',fontsize=12,ncol=2,frameon=True,title=r'$(a,b)$')
setp(l.get_title(),fontsize=14)
xlabel(r'Year')
ylabel(r'treas. yield ratio: $\frac{a\textrm{ year}}{b\textrm{ year}}$')
grid(which='major',ls=':')
grid(which='minor',ls=':',alpha=0.5)
xlim(datetime64('1960'),datetime64('2020'))
ylim(0,1.50)
ax.xaxis.set_minor_locator(LinearLocator(numticks=61))
ax.yaxis.set_minor_locator(MultipleLocator(0.1))
#ax2 = ax.twinx()
#ax2.set_ylim(ax.get_ylim())
#ax2.set_ylabel(r'junk yield ratio: $\frac{10\textrm{ year}}{\textrm{Junk}}$',color='b')
#ax2.xaxis.set_minor_locator(LinearLocator(numticks=61))
savefig('treasury_yield_ratio.png',bbox_inches='tight',dpi=300)

print('DGS1 / DGS10 last ten')
print(df.y1ratio.iloc[-10:])
print('DGS5 / DGS10 last ten')
print(df.y5ratio.iloc[-10:])
print('DGS1 / DGS5 last ten')
print(df.x1ratio.iloc[-10:])
print('DGS3 / DGS5 last ten')
print(df.x3ratio.iloc[-10:])
