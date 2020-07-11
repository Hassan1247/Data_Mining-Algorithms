#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define MINSUP 5

void prune(map<set<int>,unsigned ll int> *diNew, map<set<int>,unsigned ll int> *di, ll k){
    map<set<int>,unsigned ll int> ditmp;
    for ( auto &x:*diNew){
        ll c = 0;
        for(auto &y: x.first){
            set<int> tmp;
            tmp.insert(y);
            vector<int> temp(k);
            set_difference(x.first.begin(),x.first.end(),tmp.begin(),tmp.end(),temp.begin());
            set<int> tm(temp.begin(),temp.end());
            if (di->count(tm) == 0){
                break;
            }else{
                c++;
            }
        }
        if ( c == k + 1){
            ditmp[x.first] = 0;
        }
    }
    diNew->clear();
    for ( auto &x:ditmp){
        (*diNew)[x.first] = 0;
    }
}

void make(vector<int> *arr, ll n, ll r, ll index, vector<int> *data, ll i, map<set<int>,unsigned ll int> *diNew){
    if (index == r) { 
        for (int j = 0; j < r; j++) {
            set<int> tmp(data->begin(),data->end());
            (*diNew)[tmp] = 0;
        }
        return; 
    } 
    if (i >= n) 
        return; 
    (*data)[index] = (*arr)[i]; 
    make(arr, n, r, index + 1, data, i + 1,diNew); 

    make(arr, n, r, index, data, i + 1,diNew); 
}

int main(){
    fstream fi,fo;
    ll k = 1,c = 0;
    map<int,unsigned ll int> dict;
    map<set<int>,unsigned ll int> di;
    map<set<int>,unsigned ll int> diNew;
    vector<int> v(1);
    vector<vector<int>> list;
    fi.open("input");
    fo.open("output");
    if (!fi and !fo){
        cout << "Error in openning the files !" << endl;
        return 0;
    }
    string a;
    ll i = 0,j = 0;
    //  Read file and save the input in list
    while (getline(fi,a)){
        stringstream iss( a );
        int numb;
        list.push_back(v);
        j = 0;
        while (iss >> numb){
            if (j == 0){
                list[i][j] = numb;
            }else{
                list[i].push_back(numb);
            }
            if (dict.count(numb) == 0){
                dict[numb] = 1;
            }else{
                dict[numb]++;
            }
            j++;
        }
        i++;
    }
    // Generate frequent itemset of length 1
    for(auto& x : dict){
        if (x.second >= MINSUP){
            // cout << x.first << "," << x.second << endl;
            set<int> si;
            si.insert(x.first);
            di[si] = x.second;
            fo << x.first << "," << x.second << endl;
        }
    }
    dict.clear();
    // while k
    while(!di.empty()){
        // make the dict on new with length of k + 1
        map<set<int>,unsigned ll int>::iterator iterI;
        map<set<int>,unsigned ll int>::iterator iterJ;
        for(iterI = di.begin(); iterI != di.end(); ++iterI){
            iterJ = iterI;
            ++iterJ;
            for(;iterJ != di.end(); ++iterJ){
                // cout << iterI->first << ' ' << iterJ->first << endl;
                vector<int> tmp(k*2);
                vector<int>::iterator it;
                it = set_union(iterI->first.begin(),iterI->first.end(),iterJ->first.begin(),iterJ->first.end(),tmp.begin());
                // make sets of length k + 1 with two sets of length k 
                if (k >= 2){
                    for (auto &x:tmp){
                        if (x == 0){
                            tmp.pop_back();
                        }
                    }
                    vector<int> data(k+1);
                    make(&tmp,tmp.size(),k+1,0,&data,0,&diNew);
                }else{
                    set<int> tm(tmp.begin(),tmp.end());
                    diNew[tm] = 0;
                }
            }
        }
        // prune the dict on k + 1 with all k subsets
        if (k >= 2){
            prune(&diNew,&di,k);
        }
        
        // calculate all the frequent itemsets
        for(iterI = diNew.begin(); iterI != diNew.end(); ++iterI){
            for (ll i = 0; i < list.size(); i++){
                vector<int> tmp(iterI->first.size());
                set_difference(iterI->first.begin(),iterI->first.end(),list[i].begin(),list[i].end(),tmp.begin());
                if (tmp[0] == 0){
                    iterI->second++;
                }
            }
        }

        // remove all frequent itemsets bellow MINSUP
        di.clear();
        for(auto& x : diNew){
            if (x.second >= MINSUP){
                di[x.first] = x.second;
                for(auto &y: x.first){
                    fo << y << ' ';
                }
                fo << "," << x.second << endl;
            }
        }
        diNew.clear();
        k++;
    }
    // print diNew
    // for ( auto &x:di){
    //     for(auto &y: x.first){
    //         cout << y << ' ';
    //     }
    //     cout << endl << x.second << endl;
    // }

    // for (ll i = 0; i < list.size(); i++){
    //     for (ll j = 0 ; j < list[i].size(); j++){
    //         cout << list [i][j] << " ";
    //     }
    //     cout << endl;
    // }
    fi.close();
    fo.close();
    return 0;
}
