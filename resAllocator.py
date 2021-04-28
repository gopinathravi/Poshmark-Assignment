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
        
        for j in input_instances.keys():
            ans_dict = {}
            if flag == 0:
                counter = 0
                flag    = 1
            else:
                counter += 1
            ans_dict["region"]     = j

            ans_dict["total_cost"] = price_list[counter]
            
            ans_dict["servers"]    = []
            
            for s in range(len(server_list_map)):
                if retServers[counter][s] > 0.0:
                    sr = (server_list_map[s],retServers[counter][s])
                    ans_dict["servers"].append(sr)
            ans_item_list.append(ans_dict)

        ans_item_list = sorted(ans_item_list, key = lambda i:i["total_cost"]) 
    
    return ans_item_list