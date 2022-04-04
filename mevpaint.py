import urllib.request
import urllib.parse
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import csv
import bisect
import etherscan_api


global_block_start = 12850000
global_block_end = 13080000
london_fork = 12965000


def MEV_flashbots_analysis(block_start=global_block_start,block_end=global_block_end):#not include end
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
    flashbots_api_url = 'https://blocks.flashbots.net/v1/blocks'
    
    blockno = block_end
    data = [0 for i in range(block_end-block_start)]
    while blockno >= block_start:
        print(blockno)
        data_dict = {
            'before' : blockno,
            'limit' : 2000
        }
        data_string = urllib.parse.urlencode(data_dict)
        url = flashbots_api_url + "?" + data_string
        req = urllib.request.Request(url,headers=header) 
        content = urllib.request.urlopen(req).read()
        mp = eval(content)
        for block in mp['blocks']:
            blockno = block['block_number']
            if blockno < block_start: break
            data[blockno-block_start] = int(block['miner_reward'])
            #coinbase_transfers[blockno] = block['coinbase_transfers']
    np.save('./cache/'+'MEV_flashbots'+'.npy',data)
    
def paint_over_time(block_start=global_block_start,block_end=global_block_end,path='tmp.svg'):
    data = np.load('./cache/'+'MEV_flashbots'+'.npy',allow_pickle=True)
    data = data[block_start-global_block_start:block_end-global_block_start]
    sum = data.copy()
    cnt = data.copy()
    for i in range(len(data)-2,-1,-1):
        sum[i] += sum[i+1]
        cnt[i] = (1 if data[i]!=0 else 0) + cnt[i+1]
    x = []
    avg = []
    nonzero = []
    nonzero_avg = []
    dist = 500
    for i in range(dist,len(data)-dist):
        x.append(i+block_start)
        avg.append((sum[i-dist] - sum[i+dist]) / (dist + dist))
        nonzero.append((cnt[i-dist] - cnt[i+dist]) / (dist + dist) * 10**18)
        nonzero_avg.append((sum[i-dist] - sum[i+dist]) / (cnt[i-dist] - cnt[i+dist]))
    mx = min(2*10**18,max(data))
    tick = [block_start,london_fork,block_end]
    fig,ax = plt.subplots()
    plt.xlabel('block_number')
    plt.ylabel('MEV_private(wei)')
    #plt.yscale('log')
    plt.xlim((block_start,block_end))
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    plt.xticks(tick)
    plt.ylim((0,mx))
    plt.bar(range(block_start,block_end),data)
    plt.plot(x,avg,color='red',linewidth=.1,label='average')
    plt.legend(loc='upper right')
    plt.plot(x,nonzero,color='purple',linewidth=.1,label='nonzero proportion')
    plt.legend(loc='upper right')
    plt.plot(x,nonzero_avg,color='green',linewidth=.1,label='average of nonzero')
    plt.legend(loc='upper right')
    plt.savefig(path)
    plt.cla()
    #plt.show()

def paint_over_distribution(block_start=global_block_start,block_end=global_block_end,path='tmp.svg'):
    data = np.load('./cache/'+'MEV_flashbots'+'.npy',allow_pickle=True)
    data = data[block_start-global_block_start:block_end-global_block_start]
    data_clean = []
    for i in data:
        assert(type(i)==int)
        if (i!=0)and(i<10**18): data_clean.append(i)
    #print(len(data_clean))
    data_clean = np.array(data_clean)
    #print(min(data))
    sns.kdeplot(data,gridsize=10000)
    plt.xlim((0,10**18))
    #plt.yscale('log')
    plt.savefig(path)
    plt.cla()

#def work():
    #miner_income_analysis(block_start,block_end)
    #paint_over_time(global_block_start,global_block_end,'time_large.svg')
    #paint_over_distribution(12960000,12965000,'before_small.svg')
    #paint_over_distribution(12965000,12970000,'after_small.svg')
    #paint_over_distribution(global_block_start,london_fork,'before_large.svg')
    #paint_over_distribution(london_fork,global_block_end,'after_large.svg')


if __name__ == '__main__':
    #work()
    #paint_over_distribution()
    #print(get_block_reward(12697906))
    #print(date_to_timestamp('2/26/2020'))
    block_start = 12890000
    block_end = 13030000
    data = np.load('./cache/'+'MEV_flashbots'+'.npy',allow_pickle=True)
    MEV_flashbots = data[block_start-global_block_start:block_end-global_block_start]
    block_reward = MEV_flashbots.copy()

    timestamp = []
    blockreward_daily = []
    reader = csv.reader(open('./download/export-BlockReward.csv'))
    istitle = True
    for row in reader:
        if istitle:
            istitle = False
            continue
        timestamp.append(int(row[1]))
        blockreward_daily.append(float(row[2]))
    
    timestamp1 = []
    blockcount_daily = []
    reader = csv.reader(open('./download/export-BlockCountRewards.csv'))
    istitle = True
    for row in reader:
        if istitle:
            istitle = False
            continue
        timestamp1.append(int(row[1]))
        blockcount_daily.append(int(row[2]))
    
    l = block_start
    r = 0
    for i in range(len(timestamp)-1):
        assert(timestamp[i]==timestamp1[i])
        time = timestamp[i]
        if time < 1627084800: continue
        print(i)
        l = r
        r = etherscan_api.get_blockno_by_timestamp(timestamp[i+1])
        print(l,r)
        reward = int(blockreward_daily[i]/blockcount_daily[i]*10**5)*(10**13)
        for mid in range(l,r):
            if mid >= block_start and mid < block_end:
                block_reward[mid-block_start] = reward

    writer = csv.writer(open('tmp.csv','w'))
    rows = []
    rows.append(('blockno','MEV_flashbots','total_blockreward(except coinbase transfer)'))
    for i in range(len(MEV_flashbots)):
        rows.append((i+block_start,MEV_flashbots[i],block_reward[i]))
    writer.writerows(rows)
