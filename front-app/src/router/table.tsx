import { useLoaderData, NavLink } from "react-router-dom";
import { getTable } from "../dataConnecter";
import { useEffect, useRef, useState } from "react";
import { useIntersection } from "../utils";

export async function loader({ params }: { params: any }){
  const id = params.fileID;
  console.log(id)
  const data = await getTable(id, 0);
  return { data, fileID: id };
}

type TableResponse = {
  name: string,
  types: string,
  data: string,
  ended: string,
  chunk: string,
}

export default function TablePage(){
  const { data, fileID } = useLoaderData() as { data: TableResponse, fileID: number };
  const [ chunk, setChunk ] = useState(0);
  const [ ended, setEnded ] = useState(JSON.parse(data.ended) as boolean);
  const types = JSON.parse(data.types);
  const columns = Object.keys(types);

  const parseData = (rawData: any) => {
    const data = JSON.parse(rawData);
    const table : any[] = [];
    for(let key of Object.keys(data)){
      let row : any = {};
      for(let type of columns){
        row[type] = data[key][type];
        if (row[type] == null) row[type] = "N/A";
        if (types[type] == "datetime"){
          row[type] = new Date(row[type]).toLocaleDateString();
        }
        else if (types[type] == "complex"){
          row[type] = row[type].real + "+" + row[type].imag + "i";
        }
      }
      table.push(row);
    }
    return table;
  }

  const fileName = data.name;
  const [ content, setContent ] = useState(parseData(data.data));
  const triggerRef = useRef<HTMLTableRowElement>(null);
  const isVisible = useIntersection(triggerRef, "0px");

  useEffect(()=>{
    if (isVisible && !ended){
      console.log("Reach end");
      // Retrieve more data
      getTable(fileID, chunk+1).then((res)=>{
        setContent((c)=>[...c, ...parseData(res.data)]);
        setChunk(JSON.parse(res.chunk));
        setEnded(JSON.parse(res.ended));
      }).catch(err=>console.error(err));
    }
  }, [isVisible, chunk])

  return (
    <div className="content-center">
      <div className="header">
        <NavLink to="/">Back</NavLink>
        <h1>{fileName}</h1>
      </div>
      <div className="table-wrapper">
        <table>
          <thead>
          <tr>
            <th></th>
            { columns.map((c,i)=><th key={i}>{c}</th>) }
          </tr>
          </thead>
          <tbody>
          { content.map((t,i)=>(
            (i == content.length - 1) ?
            (<tr key={i} ref={triggerRef}>
              <td>{i+1}</td>
              { columns.map((c,j)=><td key={i*j+j}><p>{t[c]}</p></td>)}
            </tr>):
            (
              <tr key={i}>
                <td>{i+1}</td>
                { columns.map((c,j)=><td key={i*j+j}><p>{t[c]}</p></td>)}
              </tr>
            )
          )) }
          </tbody>
        </table>
      </div>
    </div>
  )
}