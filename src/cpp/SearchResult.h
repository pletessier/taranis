// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

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
