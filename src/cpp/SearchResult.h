//
// Created by pletessier on 26/05/19.
//

#ifndef CPP_TARANIS_SEARCHRESULT_H
#define CPP_TARANIS_SEARCHRESULT_H


#include <cstdint>

#include <vector>

using namespace std;

class SearchResult {

    vector<vector<int64_t>*> *knns;
    vector<vector<float>*> *dists;

public:
    SearchResult();
    ~SearchResult();

    vector<vector<int64_t> *> *getKnns() const;

    void setKnns(vector<vector<int64_t> *> *knns);

    vector<vector<float> *> *getDists() const;

    void setDists(vector<vector<float> *> *dists);


};


#endif //CPP_TARANIS_SEARCHRESULT_H
