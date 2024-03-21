#include <iostream>
#include <vector>
using namespace std;
int solve(vector<int> &arr, int index)
{
    if (index < 0)
    {
        return 0;
    }
    if (index == 0)
    {
        return arr[0];
    }
    int include = arr[index] + solve(arr, index - 2);
    int exclude = solve(arr, index - 1);
    return max(include, exclude);
}
int main()
{
    vector<int> arr;
    int n;
    cout << "Enter the number of elements in the array" << endl;
    cin >> n;
    arr.resize(n);
    cout << "Enter the elements of the array" << endl;
    for (int i = 0; i < n; i++)
    {
        cout << "Enter element " << i + 1 << ":";
        cin >> arr[i];
    }
    cout << "The result is: " << solve(arr, n - 1) << endl;
    return 0;
}