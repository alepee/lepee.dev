import { getCollection } from 'astro:content';

const visible = ({ data }: { data: { draft: boolean } }) => import.meta.env.DEV || !data.draft;

/** Published posts, newest first. */
export async function getPosts() {
	return (await getCollection('blog', visible)).sort(
		(a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
	);
}
