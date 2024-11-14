import { useLoaderData, Form, NavLink, useNavigate } from "react-router-dom";
import React, { useState } from "react";
import { getFileNames, uploadFile } from "../dataConnecter";


export async function loader(){
  const files = await getFileNames() as any[];
  if (files){
    return files.map((f)=>({name: f.filename, id: f.pk}));
  }
  return null;
}

type FileMetaData = {
  name: string,
  id: number
}

export default function FilePage(){
  const files = useLoaderData() as FileMetaData[];
  return (
    <div className="file-page-layout">
      <FileUploader></FileUploader>
      <div className="file-list-layout">
        {files && files.map((f)=>(
          <FileListItem key={f.id} fileName={f.name} fileID={f.id}></FileListItem>
        ))}
      </div>
    </div>
  );
}

function FileUploader(){
  const navigate = useNavigate();

  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) =>{
    if (e.target.files){
      setFile(e.target.files[0]);
    }
  };

  return (
    <>
    <div className="input-group">
      <input id="file" type="file" onChange={handleFileChange} accept=".csv"/>
    </div>
    { file && (
      <section>
        File details:
        <ul>
          <li>Name: {file.name}</li>
          <li>Type: {file.name}</li>
          <li>Size: {file.name}</li>
        </ul>
      </section>
    )}

    {
      file && (
        <button onClick={async ()=>{
          await uploadFile(file);
          // setFile(null);
          navigate(0);
        }} className="submit">Upload a file</button>
      )
    }
    </>
  );
}

function FileListItem({ fileName, fileID }: { fileName: string, fileID: number }){
  return (
    <div className="file-list-item">
      <NavLink to={`/table/${fileID}`}>{fileName}</NavLink>
      <Form method="post" action={`${fileID}/delete`} onSubmit={(event)=>{
        if (!confirm("Please confirm you want to remove this file")){
          event.preventDefault();
        }
      }}>
        <button type="submit">Delete</button>
      </Form>
    </div>
  );
}