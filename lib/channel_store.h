#include <map>
#include <set>

template<typename T>
class channel_store
{
  std::map<size_t, T> values_;
  std::set<size_t> initialized_channels_;

public:
  template <typename pred>
  T set_if_not_equal(T value, size_t n, size_t max_n, pred fn)
  {
      if( n < max_n)
      {
         if( initialized_channels_.find(n) == initialized_channels_.end())
         {
             values_[n] = fn();
             initialized_channels_.insert(n);
         } else {
             auto &val = values_[n];
             if( val != value)
             {
                 val = fn();
             }
         }
         return values_[n];
      }
      return T{};
  }
  T & operator[](size_t n)
  {
      return values_[n];
  }
};
