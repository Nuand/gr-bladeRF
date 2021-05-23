#include <map>

template<typename T>
class channel_store
{
  std::map<size_t, T> values_;
public:
  template <typename pred>
  T set_if_not_equal(T value, size_t n, size_t max_n, pred fn)
  {
      if( n < max_n)
      {
          auto &val = values_[n];
          if(val != value)
          {
              val = fn();
          }
          return val;
      }
      return T{};
  }
  T & operator[](size_t n)
  {
      return values_[n];
  }
};
