#ifndef __XFABRIC_DECLARATIONS_H__
#define __XFABRIC_DECLARATIONS_H__

#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/prio-queue.h"

using namespace ns3;

extern Ptr<Tracker> flowTracker;

extern std::vector<Ptr <Queue> > AllQueues;
extern std::map<uint32_t, double> flow_sizes;
extern int checkTimes;
extern std::map<uint32_t, std::vector<uint32_t> > source_flow;
extern std::map<uint32_t, std::vector<uint32_t> > dest_flow;
extern uint32_t flows_tcp;
extern uint32_t weight_change;
extern uint32_t weight_normalized;
extern bool rate_based;

extern ApplicationContainer sinkApps;

extern double kvalue;
extern uint32_t vpackets;

extern double sim_time;
extern double measurement_starttime ;
extern double prio_q_min_update_time ;
extern double gamma1_value ;
extern double xfabric_beta;
extern uint32_t flows_per_host;
extern std::string application_datarate;
extern bool delay_mark_value;

extern bool xfabric;
extern bool xfabric_price;
extern bool dctcp;
extern bool pfabric_util;
extern uint32_t hostflows;


extern double price_update_time ;
extern double xfabric_eta;
extern double xfabric_beta;
extern double guard_time;
extern double rate_update_time ;
extern double flow2_stoptime;
extern double flow1_stoptime;
extern double flow3_stoptime;
extern double flow2_starttime;
extern double flow1_starttime;
extern double flow3_starttime;

extern double dgd_a;
extern double dgd_b ;
extern double target_queue ;

extern double rcp_alpha;
extern double rcp_beta;

/* Deadline variables */
extern bool deadline_mode;
extern bool scheduler_mode_edf;
extern double deadline_mean;
extern double fraction_flows_deadline;

extern float sampling_interval ;
extern uint32_t pkt_size ;
//uint32_t max_queue_size ;
extern uint32_t max_ecn_thresh ;
extern uint32_t max_queue_size ;
//uint32_t max_ecn_thresh ;
//uint32_t max_segment_size ;
extern uint32_t max_segment_size ;
extern uint32_t ssthresh_value ;
extern std::map<std::string, uint32_t> flowids;
extern uint32_t recv_buf_size ;
extern uint32_t send_buf_size ;
extern double link_delay ; //in microseconds
extern bool margin_util_price ;

extern uint32_t N ; //number of nodes in the star
extern uint32_t skip ;
extern std::string queue_type;
extern double epoch_update_time ;
extern bool pkt_tag, onlydctcp, wfq, dctcp_mark;
extern bool strawmancc ;
extern std::string empirical_dist_file_DCTCP_heavy;
extern std::string empirical_dist_file;
extern double UNKNOWN_FLOW_SIZE_CUTOFF;
extern std::string empirical_dist_file_DCTCP_light;
extern Ptr<EmpiricalRandomVariable>  SetUpEmpirical(std::string fname);
extern void scheduler_wrapper(uint32_t);

extern std::string link_twice_string ;

extern NodeContainer allNodes;
extern NodeContainer bottleNeckNode; // Only 1 switch
extern NodeContainer sourceNodes;    
extern NodeContainer clientNodes;    
extern NodeContainer sinkNodes;

extern double ONEG ;
extern double link_rate ;
extern std::string link_rate_string ;

extern double load ;
extern double controller_estimated_unknown_load ;
extern double meanflowsize ; // what TBD?

/* Application configuration */
//ApplicationContainer apps;
extern std::vector< Ptr<Socket> > ns3TcpSockets;
extern std::string prefix;
extern uint32_t util_method ;
extern uint16_t *ports;

extern std::map<uint32_t, double> flowweights;

extern Ptr<PacketSink> sinkInstallNode(uint32_t sourceN, uint32_t sinkN, uint16_t port, uint32_t flow_id, double startTime, uint32_t numBytes, uint32_t tcp);
extern void sinkInstallNodeEvent(uint32_t sourceN, uint32_t sinkN, uint16_t port, uint32_t flow_id, double startTime, uint32_t numBytes, uint32_t tcp);


extern double getDeadline(double start_time, double flow_size, Ptr<ExponentialRandomVariable> exp, Ptr<UniformRandomVariable> deadline_decision, uint32_t flow_num);

Ptr<ExponentialRandomVariable> getDeadlineRV();
Ptr<UniformRandomVariable> getDecisionRV();

extern CommandLine addCmdOptions(void);
extern void common_config(void);
extern void setUpMonitoring(void);
extern void CheckIpv4Rates (NodeContainer &allNodes);
extern void printlink(Ptr<Node> n1, Ptr<Node> n2);
extern Ipv4InterfaceContainer assignAddress(NetDeviceContainer dev, uint32_t subnet_index);
extern void CheckQueueSize (Ptr<Queue> queue);
void setuptracing(uint32_t sindex, Ptr<Socket> skt);
void run_scheduler(FlowData fdata, uint32_t eventtype);
void run_scheduler_edf(FlowData fdata, uint32_t eventtype);

extern bool host_compensate;
extern double fct_alpha;

extern std::string fabric_datarate;
extern std::string edge_datarate;
extern double fabricdelay, edgedelay;
extern bool packet_spraying, flow_ecmp;

// number of nodes for leaf-spine
//uint32_t num_spines = 4, num_leafs = 9, num_hosts_per_leaf = 16;
extern uint32_t num_spines, num_leafs, num_hosts_per_leaf;
extern NodeContainer spines, leafnodes, hosts;

extern const uint32_t max_flows;
extern uint32_t arg_max_flows;

extern double dt_val;
extern double kvalue_price;
extern double kvalue_rate;
extern double kvalue_measurement;

extern void dump_config(void);
extern bool price_multiply;
extern uint32_t number_flows;
extern bool desynchronize;
extern double multiplier;
extern std::string opt_rates_file;
typedef struct OptDataRate_ {
  uint32_t flowid;
  double datarate;
  //OptDataRate(uint32_t f, double d) {flowid = f; datarate = d;}
} OptDataRate;


//extern std::map<uint32_t, std::vector< OptDataRate> > opt_drates;
extern std::map<uint32_t, std::map<uint32_t, double> > opt_drates;
extern uint32_t epoch_number;
extern EventId next_epoch_event;
void startflowwrapper(std::vector<uint32_t>, std::vector<uint32_t>);
extern std::vector<uint32_t> sourcenodes;//(max_system_flows, 0);
extern std::vector<uint32_t> sinknodes;//(max_system_flows, 0);
extern uint32_t ninety_fifth;
extern bool alpha_fair_rcp;

extern double LastEventTime;
extern std::vector<Ptr<PacketSink> >sink_objects;
extern std::list<uint32_t> flows_to_start;
extern std::list<uint32_t> flows_to_stop;
extern std::list<uint32_t> event_list;
extern bool mptcp;
extern uint32_t num_subflows;
extern bool bwe_enable;
extern uint32_t num_events;

#endif 
