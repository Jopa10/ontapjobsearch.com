import { slices } from "@/data/getSlice"

export default function Page({
  params,
}: {
  params: { city: string; role: string }
}) {
  const city = decodeURIComponent(params.city).toLowerCase()
  const role = decodeURIComponent(params.role).toLowerCase()
  const key = `${city}/${role}`

  const slice = (slices as Record<string, any>)[key]

  if (!slice) {
    return (
      <div style={{ padding: 40 }}>
        <div>
          <b>Not found</b>
        </div>
        <div>
          Looking for key: <code>{key}</code>
        </div>
        <div style={{ marginTop: 12 }}>
          Available keys (first 50):
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {Object.keys(slices).slice(0, 50).join("\n")}
          </pre>
        </div>
      </div>
    )
  }

  const job = slice.jobs?.[0]

  return (
    <main style={{ padding: 40 }}>
      <h1>
        {slice.role} jobs in {slice.city}
      </h1>

      <h2>{job?.title}</h2>
      <p>{job?.company}</p>
      <p>{job?.location}</p>
      <p>{job?.salary}</p>
    </main>
  )
}




