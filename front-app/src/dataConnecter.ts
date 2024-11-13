export async function getData(){
  const url = "http://127.0.0.1:8000/data/dataset";
  try {
    const response = await fetch(url, {
      method: "GET"
    });
    console.log(response);
    if (!response.ok){
      console.log("Fetch failed");
      return;
    }
    const json = await response.json();
    console.log(json);
  }
  catch (error: any){
    console.error(error.message);
  }
}