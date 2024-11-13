export function urlPrefix(url: string){
  return "http://127.0.0.1:8000/" + url;
}

export async function getFileNames(){
  const url = urlPrefix("data/dataset");
  try {
    const response = await fetch(url, {
      method: "GET"
    });
    if (!response.ok){
      console.error("Fetch failed");
      return null;
    }
    const json = await response.json();
    return json
  }
  catch (error: any){
    console.error(error.message);
    return null;
  }
}

export async function uploadFile(file: File){
  if (file){
    const formData = new FormData();
    formData.append('file', file);
    formData.append('filename', file.name);

    try{
      const result = await fetch(urlPrefix("data/dataset"), {
        method: "POST",
        body: formData,
      });
      
      if (result.status === 200){
        console.log("Upload success");
      }
      else{
        console.error("Upload failed");
      }
    }
    catch (error){
      console.error(error);
    }
  }
}

export async function deleteFile(id: number){
  const formData = new FormData();
  formData.append("id", id.toString());
  const result = await fetch(urlPrefix("data/dataset"), {
    method: "DELETE",
    body: formData
  })
  return result.status === 200;
}