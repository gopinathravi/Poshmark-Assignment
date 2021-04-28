input_server_instances = {"us-east":{
                    "large":0.12,
                    "xlarge":0.23,
                    "2xlarge":0.45,
                    "4xlarge":0.774,
                    "8xlarge":1.4,
                    "10xlarge":2.82},
                   "us-west":{
                     "large":0.14,
                     "2xlarge":0.413,
                     "4xlarge":0.89,
                     "8xlarge":1.3,
                     "10xlarge":2.97},
                     "asia":{
                         "large":0.11,
                         "xlarge":0.20,
                         "4xlarge":0.67,
                         "8xlarge":1.18
                     }}

server_types_map = ["large","xlarge","2xlarge","4xlarge","8xlarge","10xlarge"]


#looks like knapsack problem but since price is in float can't access index and can't apply DP
#Use case 1
def serverInstanceWithoutCPU(price,cost_list,server_list):
    i         = len(cost_list)
    ans       = [0 for val in range(i)]
    cost      = 0
    remaining_price = price
    while i >= 0:
        if cost_list[i-1] < 0:
            i = i-1
        elif cost_list[i-1] <= remaining_price:
            remaining_price = remaining_price - cost_list[i-1]
            if server_list[i-1] > 0:
                ans[i-1] = ans[i-1] + 1
        else:
            i = i-1

    return ans

#Use case 2
def serverInstanceWithOutPrice(no_cpu,sum_li,server_list):

    i   = len(server_list)
    ans = [0 for q in range(i)]
    while i >= 0 :
        if no_cpu > sum_li :
            if sum_li > 0:
                incr = no_cpu//sum_li                
                no_cpu = no_cpu % sum_li                
            else :
                ans[0] = ans[0] + 1
                break
            for x in range(i):
                if server_list[x] > 0:
                    ans[x] += incr
                else:
                    ans[x] = 0
        else :
            if server_list[i-1] > 0:
                sum_li = sum_li - server_list[i-1]
            i = i - 1            
    return ans

#Use case 3
def serverInstanceWithCpuPrice(no_cpu,sum_li,server_list,cost_list,max_price):
    i           = len(server_list)
    ans         = [0 for q in range(i)]
    price_margin = [0 for p in range(i)]
    while sum(price_margin) <= max_price :					
        if no_cpu > sum_li :	
            if(sum(cost_list[0:i]) <= max_price):				
                if sum_li > 0:
                    incr   = no_cpu // sum_li
                    no_cpu = no_cpu % sum_li
                else:
                    ans[0] = ans[0] + 1
                    break
                for x in range(i):
                    if server_list[x] > 0 :							
                        ans[x] += incr
                    else:
                        ans[x] = 0
                price_margin = [a*b for a,b in zip(ans,cost_list)]
                if sum(price_margin) > max_price:
                    for x in range(i):
                        if server_list[x] > 0 :				
                            ans[x] -= incr
                    sum_li = sum_li - server_list[i-1]
                    i = i - 1
                                        
            else:
                if server_list[i-1] > 0:
                    sum_li = sum_li - server_list[i-1]
                i = i -1
        else:
            if server_list[i-1] > 0:
                sum_li = sum_li - server_list[i-1]
            i = i -1
            
    return ans


# Util function to calculate total cost and server list
def getServerCombination(server_combination_data,total_cost,cost_list_h,server_combination):

    server_combination_data = [float(val) for val in server_combination_data]
    
    total_cost.append([a*b for a,b in zip(server_combination_data,cost_list_h)])
    
    server_combination_data = [int(val) for val in server_combination_data]

    server_combination.append(server_combination_data)

    return server_combination,total_cost

#preparing the instance cost list
def fetchServerCostList(server_types_map,hours,cpus,price):
    server_combination_data = []
    server_combination   = []
    total_cost           = []
    for k,v in input_server_instances.items():

        server_list = [0 for s in range(len(server_types_map))]

        cost_list = [0 for s in range(len(server_types_map))]
        
        for i in range(len(server_types_map)):
            if server_types_map[i] in list(v.keys()):
                server_list[i] = 2**i
                cost_list[i]   = v[server_types_map[i]]
            else:
                cost_list[i]   = -1
        
        cost_list_h = [h*hours for h in cost_list]

        sum_server_list = sum(server_list)
             
        if cpus == 0:
            server_combination_data = serverInstanceWithoutCPU(price,cost_list_h,server_list)

        elif price == 0.0:
            server_combination_data = serverInstanceWithOutPrice(cpus,sum_server_list,server_list)

        else:
            server_combination_data = serverInstanceWithCpuPrice(cpus,sum_server_list,server_list,cost_list_h,price)
        
        ServerList,TotalCost = getServerCombination(server_combination_data, total_cost, cost_list_h, server_combination)
    
    return TotalCost,ServerList  

def get_costs(hours,cpus,price):
    
    price_list = []
    ans_item_list  = []
    #Base conditions
    if hours is None or hours < 0:
        print("Invalid input (hour)")
        return
    elif price < 0.0:
        print ("Invalid input (price)")
        return
    elif cpus < 0:
        print ("Invalid input (cpus)")
        return
    else:
        totalCost,retServers = fetchServerCostList(server_types_map,hours,cpus,price)
        flag = 0
        
        for i in range(len(totalCost)):
            price_list.append(sum(totalCost[i]))
        
        for j in input_server_instances.keys():
            ans_dict = {}
            if flag == 0:
                counter = 0
                flag    = 1
            else:
                counter += 1
            ans_dict["region"]     = j

            ans_dict["total_cost"] = price_list[counter]
            
            ans_dict["servers"]    = []
            
            for s in range(len(server_types_map)):
                if retServers[counter][s] > 0.0:
                    sr = (server_types_map[s],retServers[counter][s])
                    ans_dict["servers"].append(sr)
            ans_item_list.append(ans_dict)

        ans_item_list = sorted(ans_item_list, key = lambda i:i["total_cost"]) 
    
    return ans_item_list
