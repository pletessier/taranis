// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.
#include "SearchResult.h"

SearchResult::SearchResult(){

    knns = new vector<vector<int64_t>*>();
    dists = new vector<vector<float>*>();

}

SearchResult::~SearchResult() = default;

vector<vector<int64_t> *> *SearchResult::getKnns() const {
    return knns;
}

void SearchResult::setKnns(vector<vector<int64_t> *> *knns) {
    SearchResult::knns = knns;
}

vector<vector<float> *> *SearchResult::getDists() const {
    return dists;
}

void SearchResult::setDists(vector<vector<float> *> *dists) {
    SearchResult::dists = dists;
}
