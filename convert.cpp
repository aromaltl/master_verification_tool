#include <iostream>
#include "json.hpp"
#include "pybind11/pybind11.h"
#include <string>

namespace py = pybind11;
using json = nlohmann::json;

std::string convert_format(std::string & u, int total_frames) {
    json j = json::parse(u);
    json n;
    // json fin;
    // std::map<std::string,std>
    // fin["Assets"]={};
    for (int i=0; i<total_frames;i+=2){ 
        for (const auto& v1 : j[std::to_string(i)].items()) {

            if (!n.contains(v1.key() )){n[v1.key()]={};}


            for (const auto& v2 : v1.value().items()){

                if (!n[v1.key()].contains(v2.value().at(0))){n[v1.key()][v2.value().at(0)]={};}

                n[v1.key()][v2.value().at(0)].push_back({i,v2.value().at(1),v2.value().at(2)});
            }
            if (n[v1.key()].empty()){n.erase(v1.key());}
            // std::cout << "Key: " << key << ", Value: " << value << std::endl;
    }
    }
    // int s = 0;
    // for (const auto & v1 : n.items()){
    //     for (const auto & v2 : v1.value().items()){
    //         s = std::max(0,int(n[v1.key()][v2.key()].size())-3);

    //         std::cout<<n[v1.key()][v2.key()][s]<<":"<<s<<" ";
    //         // fin["Assets"].append({})
    //     }
    // }

    return n.dump();
}
// int addd(py::int_ &i ) {
//     // int i = ii.cast<int>();
//     // return 0;
//     i=i+1;
//     // ii=i;
//     return i;
   
    // return i ;
// }
PYBIND11_MODULE(convert, m) {
    m.doc() = "convert format"; // optional module docstring
    m.def("convert_format", &convert_format, "A function that adds two numbers");
    // m.def("addd", &addd, "A function that adds two numbers");
}
