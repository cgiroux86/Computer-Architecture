function fetchFromApi(url, setState) {
  axios
    .get(url)
    .then((res) => setState(res))
    .catch((err) => console.log(err));
}

useEffect(() => {
  fetchFromApi("www.swapi1.com", setPlanets);
  fetchFromApi("www.swapi2.com", setPeople);
  setFetching(false);
}, []);
