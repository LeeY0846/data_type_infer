import { useLoaderData } from "react-router-dom";
import { getTable } from "../dataConnecter";

export async function loader({ params }: { params: any }){
  const id = params.fileID;
  console.log(id)
  const data = await getTable(id);
  return { data };
}

export default function TablePage(){
  const { data } = useLoaderData() as { data: { types: string } };
  console.log(data);

  return (
    <h1>{data.types}</h1>
  )
}